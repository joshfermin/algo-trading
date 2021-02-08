from algo_trading.exchange.exchange_context import ExchangeContext
from algo_trading.exchange.robinhood_actions import RobinhoodActions

def main():
    exchange_actions = ExchangeContext(RobinhoodActions())

    print(exchange_actions.get_account_profile('crypto_buying_power'))
    # scheduler = BlockingScheduler(timezone=utc)

    # for symbol in SYMBOLS_TO_TRACK:
    #     scheduler.add_job(record_data, 'cron', [symbol[0], symbol[1], 86400, 'day'], day="*")
    #     scheduler.add_job(record_data, 'cron', [symbol[0], symbol[1], 3600, 'hour'], hour="*")
    #     scheduler.add_job(record_data, 'cron', [symbol[0], symbol[1], 300, 'five_minutes'], minute="*/5")
    #     scheduler.add_job(record_data, 'cron', [symbol[0], symbol[1], 60, 'one_minute'], minute="*")
    
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     pass


if __name__ == '__main__':
    main()
