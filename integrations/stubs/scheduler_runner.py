import os, time, logging, datetime as dt

def weekly_report_job():
    logging.info("[weekly_report_job] %s", dt.datetime.utcnow().isoformat() + "Z")

def metrc_poll_job():
    if not all([os.getenv("METRC_VENDOR_KEY"), os.getenv("METRC_USER_KEY"), os.getenv("METRC_LICENSE_NUMBER")]):
        logging.info("[metrc_poll_job] METRC not configured; skipping")
        return
    logging.info("[metrc_poll_job] (read-only) poll placeholder")

if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("SCHEDULER_LOG_LEVEL","INFO"))
    if os.getenv("SCHEDULER_ENABLED","true").lower() not in ("1","true","yes","on"):
        print("Scheduler disabled via SCHEDULER_ENABLED")
        raise SystemExit(0)
    interval = int(os.getenv("SCHEDULER_POLL_INTERVAL_SEC","300"))
    logging.info("Scheduler started; interval=%s sec", interval)
    while True:
        weekly_report_job()
        metrc_poll_job()
        time.sleep(interval)
