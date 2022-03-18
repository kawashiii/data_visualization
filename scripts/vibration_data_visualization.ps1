$MyPath = Split-Path $MyInvocation.MyCommand.Path
python $MyPath\vibration_data_visualization.py $args[0]