# 
# move to a utils function
# 
def handle_time_period(total_historicals, start_date=None, end_date=None):
    offset = 336
    # offset = 10
    start_index = offset
    end_index = len(total_historicals)

    # handle start and end day to find the corresponding indexes in historical crypto data
    if start_date:
        start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        start_date_index = [historical['begins_at'] for historical in total_historicals].index(start_date_str)
        start_index = start_date_index - offset

    if end_date:
        end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_index = [historical['begins_at'] for historical in total_historicals].index(end_date_str)

    return total_historicals[start_index:end_index]