generate_APFD_table <- function(table_data,ga_name){
  
  outputFile <- paste0("../../data/tables/ga-vs-baseline.tex")
  unlink(outputFile)
  
  # Redirect cat outputs to file
  sink(outputFile, append = TRUE, split = TRUE)
  cat("\\begin{tabular}{ l l | c c cl | c c c}\n")
  cat("\\hline", "\n")
  cat("\\textbf{Project}", "&", 
      "\\textbf{GA Config.}", "&",
      "\\multicolumn{3}{c|}{\\textbf{Vs. Random}}", "&",
      "\\multicolumn{3}{c}{\\textbf{Vs. Greedy}}")
  cat("\\hline", "\n")
  cat(" \\\\", "\n")
  cat(" ", "&", 
      " ", "&", 
      "$\\hat{A}_{12}$", "&",
      "p", "&",
      "Magnitude", "&",
      "$\\hat{A}_{12}$", "&",
      "p", "&",
      "Magnitude")
  cat(" \\\\", "\n")
  
  benchmarks <- unique(greedy_df$benchmark)
  for(ben in benchmarks){
    config <- ga_name
    temp <- table_data %>%
      filter(benchmark == ben & config.baseline == "random")
    
    rand_estimate <- formatC(temp$VD.estimate[1], digits=1, format="f", big.mark = ',')
    rand_p <- formatC(temp$wilcox.test.pvalue[1],  format="g", big.mark = ',')
    rand_mag <- temp$VD.magnitude[1]
    
    temp <- table_data %>%
      filter(benchmark == ben & config.baseline == "Greedy")
    
    greedy_estimate <- formatC(temp$VD.estimate[1], digits=1, format="f", big.mark = ',')
    greedy_p <- formatC(temp$wilcox.test.pvalue[1],  format="g", big.mark = ',')
    greedy_mag <- temp$VD.magnitude[1]
    
    cat(ben, "&",
        config, "&",
        rand_estimate, "&",
        rand_p, "&",
        rand_mag, "&",
        greedy_estimate, "&",
        greedy_p, "&",
        greedy_mag)
    
    cat(" \\\\", "\n")
  }
  cat("\\hline", "\n")
  cat("\\end{tabular}")
  
  # Restore cat outputs to console
  sink()
}