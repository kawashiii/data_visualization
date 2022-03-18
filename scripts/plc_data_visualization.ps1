$MyPath = Split-Path $MyInvocation.MyCommand.Path
python $MyPath\plc_data_visualization.py $args[0]