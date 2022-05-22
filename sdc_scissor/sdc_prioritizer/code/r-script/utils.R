fixBenchmarkNames <- function(df){
  df$benchmark <- ifelse(df$benchmark == "DriverAI_Complete", "DeepDriving", df$benchmark)
  df$benchmark <- ifelse(df$benchmark == "BeamNG_RF_1_Complete", "BeamNG.AI.AF1", df$benchmark)
  df$benchmark <- ifelse(df$benchmark == "BeamNG_RF_1_5_selected", "BeamNG.AI.AF1.5", df$benchmark)
  return(df)
}


scalar3 <- function(x) {(x-min(x)) / (max(x) - min(x))}