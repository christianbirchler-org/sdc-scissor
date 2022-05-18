

plotBoxPlot_APFD <- function(plot_df,l){
  p <- 	ggplot(plot_df, aes(x=factor(config,levels = c("MO-SDC-Prioritizer","SO-SDC-Prioritizer","Greedy","random")), y=APFD, fill=factor(config))) + 
    scale_colour_grey(start = 0, end = .9) +
    geom_boxplot() +
    xlab("") + 
    ylab(l) + 
    guides(fill=FALSE) +
    facet_grid(. ~ benchmark, margins = TRUE) + theme(axis.text.x = element_text(angle = 90, size = 12, face = "bold", margin = margin(t = 10, r = 0, b = 0, l = 0)), axis.text.y = element_text(size = 10, face="bold"), strip.text.x = element_text(size = 10, face="bold")) +
    stat_summary(fun.y=mean, geom="point", shape=23, size=2, fill = 'white')
  return(p)
}


plotBoxPlot_time <- function(ga_time_df,l){
  p <- 	ggplot(ga_time_df, aes(x=factor(config,levels = unique(ga_time_df$config)), y=elapsed_time, fill=factor(config))) + 
    scale_colour_grey(start = 0, end = .9) +
    geom_boxplot() +
    xlab("") + 
    ylab(l) + 
    guides(fill=FALSE) +
    facet_grid(. ~ benchmark, margins = TRUE) + theme(axis.text.x = element_text(angle = 90, size = 12, face = "bold", margin = margin(t = 10, r = 0, b = 0, l = 0)), axis.text.y = element_text(size = 10, face="bold"), strip.text.x = element_text(size = 10, face="bold"))  +
    stat_summary(fun.y=mean, geom="point", shape=23, size=2, fill = 'white')
  return(p)
}


plotBoxPlot_pareto<- function(df){
  p <- ggplot(df, aes(x = factor(benchmark,levels = unique(df$benchmark)), y = rate)) +
    geom_boxplot() +
    stat_summary(fun.y=mean, geom="point", shape=23, size=2, fill = 'white') +
    xlab("") + 
    ylab("Better than greedy non-dominated solutions") +
    theme(axis.text.x = element_text(angle = 0, size = 12, face = "bold", margin = margin(t = 10, r = 0, b = 0, l = 0)), axis.text.y = element_text(size = 10, face="bold"), strip.text.x = element_text(size = 10, face="bold"))
  return(p)
}

