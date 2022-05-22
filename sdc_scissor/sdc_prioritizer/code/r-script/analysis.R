library(dplyr)
library(effsize)
library(ggplot2)
library(readr)
library(topsis)

source('plot.r')
source('table.r')
source('utils.r')

benchmarks <- c("BeamNG.AI.AF1", "BeamNG.AI.AF1.5", "DeepDriving")
GA_configs = c("SO-SDC-Prioritizer","MO-SDC-Prioritizer")
baseline_configs = c("random", "Greedy")
CONFIGS <- c(GA_configs, baseline_configs)

# Read dataframes
df <- read.csv("../../data/mo-results.csv", stringsAsFactors = FALSE)
single_df <- read.csv("../../data/s-results.csv", stringsAsFactors = FALSE)
greedy_df <- read.csv("../../data/greedy_results.csv", stringsAsFactors = FALSE)

# Fix benchmark names
df <- fixBenchmarkNames(df)
single_df <- fixBenchmarkNames(single_df)
greedy_df <- fixBenchmarkNames(greedy_df)


######## Merge dataframes to have oe dataframe with all of the configs ######## 

# Select the compromise solution
knee_points <- df %>%
  group_by(config,benchmark, execution_id) %>%
  mutate(diversity_norm = scalar3(diversity), cost_norm = scalar3(cost)) %>%
  mutate(utopia_cost_dist = (cost_norm - min(cost_norm)), utopia_diversity_dist = diversity_norm - min(diversity_norm)) %>%
  mutate(utopia_dist = sqrt(utopia_diversity_dist^2 + utopia_cost_dist^2)) %>%
  filter(utopia_dist == min(utopia_dist)) %>%
  summarise(APFD = min(APFD), elapsed_time = min(elapsed_time) , solution_id = solution_id)


ready_df <- knee_points %>%
  select(benchmark,config,execution_id,APFD,elapsed_time) %>%
  filter(config == "mo-10_feature_GA") 

ready_df <- rbind(ready_df, single_df %>%
                    select(benchmark,config,execution_id,APFD,elapsed_time)%>%
                    filter(config == "10_feature_GA"))


## Prepare random df
rand_df <- df %>%
  group_by(benchmark,execution_id) %>%
  summarise(APFD = mean(avg_rand_APFD),
            elapsed_time = 0)
rand_df$config = "random"
rand_df <- rand_df[, c(1,5,2,3,4)]


ready_df<-rbind(ready_df,rand_df)


# Add Greedy df
for(row in 1:(nrow(greedy_df))){
  benchmark = greedy_df[[row, 'benchmark']]
  print(benchmark)
  config = greedy_df[[row, 'config']]
  APFD = greedy_df[[row, 'APFD']]
  elapsed_time = greedy_df[[row, 'elapsed_time']]
  
  for(index in 1:30){
    ready_df[nrow(ready_df) + 1,] = list(benchmark,config,index, APFD,elapsed_time)
  }
}

# 10 features GA rename
ready_df$config <- ifelse(ready_df$config == "10_feature_GA", "SO-SDC-Prioritizer", ready_df$config)
ready_df$config <- ifelse(ready_df$config == "mo-10_feature_GA", "MO-SDC-Prioritizer", ready_df$config)

################################ 





######## RQ2 ########

# boxplots and summaries
p <- plotBoxPlot_APFD(ready_df,"APFD")
ggsave(plot = p, filename = "../../data/figures/APFD.pdf", width=210, height=120, units = "mm" )


summary_apfd <- ready_df %>%
  group_by(config,benchmark) %>%
  summarise(avgAPFD = mean(APFD), minAPFD = min(APFD), maxAPFD = max(APFD)) %>%
  mutate(improvement = "1") 


summary_apfd <- summary_apfd %>%
  inner_join(summary_apfd, by=c("improvement")) %>%
  filter(config.x != config.y & benchmark.x == benchmark.y) %>%
  mutate(improvement = avgAPFD.x - avgAPFD.y,
         min_max_improvement = minAPFD.x - maxAPFD.y)%>%
  filter(improvement >=0)
  
summary_apfd_configs <- ready_df %>%
  group_by(config) %>%
  summarise(avgAPFD = mean(APFD), minAPFD = min(APFD), maxAPFD = max(APFD)) %>%
  mutate(improvement = "1") 


summary_apfd <- summary_apfd %>%
  inner_join(summary_apfd, by=c("improvement")) %>%
  filter(config.x != config.y & benchmark.x == benchmark.y) %>%
  mutate(improvement = avgAPFD.x - avgAPFD.y,
         min_max_improvement = minAPFD.x - maxAPFD.y)%>%
  filter(improvement >=0)


# Statistical tests

# compare each GA against baselines



statistics_df <- ready_df %>%
  inner_join(ready_df, by = c('benchmark'), suffix = c('.ga',".baseline")) %>%
  filter(config.ga %in% GA_configs & config.baseline %in% baseline_configs &
        execution_id.ga == execution_id.baseline) %>%
  group_by(benchmark, config.ga, config.baseline) %>%
  summarise(VD.magnitude = VD.A(APFD.ga, APFD.baseline)$magnitude,
            VD.estimate = VD.A(APFD.ga, APFD.baseline)$estimate,
            wilcox.test.pvalue = wilcox.test(APFD.ga, APFD.baseline)$p.value,
            avg.ga = mean(APFD.ga),
            avg.bl = mean(APFD.baseline))

# Save it as a latex table
for (GA_config in GA_configs) {
  temp_df <- statistics_df %>%
    filter(config.ga == GA_config)
  generate_APFD_table(temp_df,GA_config)
}

# Save it as a csv file
write_csv(statistics_df,"vsbl.csv")

# Compare GAs

statistics_df <- ready_df %>%
  inner_join(ready_df, by = c('benchmark'), suffix = c('.mo',".so")) %>%
  filter(config.mo == "MO-SDC-Prioritizer" & config.so == "SO-SDC-Prioritizer" &
           execution_id.mo == execution_id.so)%>%
  group_by(benchmark, config.mo, config.so) %>%
  summarise(VD.magnitude = VD.A(APFD.mo, APFD.so)$magnitude,
            VD.estimate = VD.A(APFD.mo, APFD.so)$estimate,
            wilcox.test.pvalue = wilcox.test(APFD.mo, APFD.so)$p.value,
            avg.mo = mean(APFD.mo),
            avg.bl = mean(APFD.so))
  

# save as csv file
write_csv(statistics_df,"gavsga.csv")



# Find the median results for each benchmark and each config

mo_df <- knee_points %>%
  select(benchmark,config,execution_id,solution_id,APFD) %>%
  filter(config == "mo-10_feature_GA") 

mo_df$config <- "MO-SDC-Prioritizer"
  

so_df <- ready_df %>%
  filter(config == "SO-SDC-Prioritizer") %>%
  select(benchmark,config,execution_id,APFD) %>%
  mutate(solution_id = 1)

interesting_GA_df <- rbind(mo_df,so_df)


median_df <- interesting_GA_df[FALSE,]
for (conf in GA_configs){
  print(conf)
  for(ben in benchmarks){
    temp <- interesting_GA_df %>%
      filter(benchmark == ben && config == conf) %>%
      arrange(APFD)
    median_row <- temp[16,]
    median_df[nrow(median_df) + 1,] <- median_row
  }
}


median_df <- median_df %>%
  inner_join(median_df, by=c("benchmark"), suffix = c(".so",".mo")) %>%
  filter(config.so == "SO-SDC-Prioritizer" &
           config.mo == "MO-SDC-Prioritizer") %>%
  select(benchmark,execution_id.so,execution_id.mo,solution_id.mo)


write_csv(median_df,"medians_APFDc.csv")

################################ 


######## RQ3 ########

## consumed time plot
### internal assessment

time_consumed_summary_config <- ready_df %>%
  group_by(config) %>%
  summarise(avg_time = mean(elapsed_time))


time_consumed_summary_dataset <- ready_df %>%
  group_by(config,benchmark) %>%
  summarise(avg_time = mean(elapsed_time))

p <- plotBoxPlot_time(ready_df %>% filter(config != "random"),"Consumed Time (Seconds)")
ggsave(plot = p, filename = "../../data/figures/consumed_time.pdf",  width=190, height=120, units = "mm" )




################################ 


######## Pareto front ########

df2 <- df %>%
  group_by(config,benchmark, execution_id) %>%
  mutate(best = ifelse(APFD == max(APFD),TRUE,FALSE)) %>%
  filter(config == "mo-10_feature_GA")
pareto_vs_greedy <- df2 %>%
  left_join(greedy_df, by = c("benchmark"), suffix = c(".mo",".greedy")) %>%
  filter(config.mo == "mo-10_feature_GA" && config.greedy == "Greedy") %>%
  mutate(better = ifelse(APFD.mo > APFD.greedy,TRUE,FALSE),
         better_counter = ifelse(APFD.mo > APFD.greedy,1,0))



better_rate <- pareto_vs_greedy %>%
  group_by(benchmark, config.mo, execution_id) %>%
  summarise(rate = sum(better_counter)/n())

p <- plotBoxPlot_pareto(better_rate)
ggsave(plot = p, filename = "../../data/figures/better_rate.pdf",  width=250, height=100, units = "mm" )


better_rate <- better_rate %>%
  group_by(benchmark)%>%
  summarise(avg_apfd = mean(rate))


better_rate <- pareto_vs_greedy %>%
  group_by(better) %>%
  summarise(rate = n()/nrow(pareto_vs_greedy))





knee_points <- df %>%
  group_by(config,benchmark, execution_id) %>%
  mutate(diversity_norm = scalar3(diversity), cost_norm = scalar3(cost)) %>%
  mutate(utopia_cost_dist = (cost_norm - min(cost_norm)), utopia_diversity_dist = diversity_norm - min(diversity_norm)) %>%
  mutate(utopia_dist = sqrt(utopia_diversity_dist^2 + utopia_cost_dist^2)) %>%
  filter(utopia_dist == min(utopia_dist)) %>%
  summarise(APFD = min(APFD), elapsed_time = min(elapsed_time) , solution_id = solution_id, cost = cost, diversity = diversity)


exec_id <- 2

for (bench in benchmarks){
  df2 <- df %>%
    group_by(config,benchmark, execution_id) %>%
    mutate(best = ifelse(APFD == max(APFD),TRUE,FALSE)) %>%
    filter(config == "mo-10_feature_GA" & benchmark == bench, execution_id == exec_id)
  
  # test <- df2 %>%
  #   ungroup() %>%
  #   select(cost, diversity)
  # test$diversity <- -test$diversity
  # test_mat <- as.matrix(test)
  # 
  # w <- c(3, 1)
  # i <- c("-", "+")
  # res <-topsis(test_mat, w, i) %>%
  #   filter(rank == min(rank))
  # row <- res[1,]$alt.row
  # 
  # best_cost <- test_mat[row, 'cost']
  # best_diversity <- test_mat[row, 'diversity']
  # group_by(execution_id) %>% top_n(1, APFD)
  # 
   max <- df2 %>% group_by(execution_id) %>% top_n(1, APFD)
  # max_score <- df2 %>% group_by(execution_id) %>% top_n(1, score)
  
  
  mid <- greedy_df %>% filter(benchmark == bench)
  mid <- mid$APFD
  
  mid <- mean(df2$APFD)
  
  
  
  knee_p <- knee_points %>% 
    filter(benchmark == bench & config == "mo-10_feature_GA" & execution_id == exec_id)
  #   scale_fill_gradient2(midpoint=mid, low="red", mid="white", 
  p <- ggplot(df2, aes(x=cost, y=-diversity, fill=APFD))+
    geom_point(shape = 21, size=3, alpha=0.75) +
    scale_fill_gradient( low="red", 
                         high="blue", space = "Lab")+
   geom_point(data = max, aes(x=cost, y=-diversity), colour="orange",  size=5, shape = 18) +
    #    geom_point(data = max_score, aes(x=cost, y=-diversity), colour="green",  size=5, shape = 18)+
    #    geom_point(aes(x=best_cost, y=best_diversity), colour="black", size = 5, shape = 18) +
    geom_point(data = knee_p, aes(x=cost, y = -diversity), colour="yellow", size = 5, shape = 18) +
    ylab("Diversity") +
    xlab("Execution Cost") +
    theme(axis.text.x = element_text(angle = 0, size = 12, face = "bold", margin = margin(t = 10, r = 0, b = 0, l = 0)), axis.text.y = element_text(size = 10, face="bold"), strip.text.x = element_text(size = 10, face="bold"))
  
  ggsave(plot = p, filename = paste0("../../data/figures/preto-front-",bench,".pdf"), width=250, height=100, units = "mm" )
  
}




 