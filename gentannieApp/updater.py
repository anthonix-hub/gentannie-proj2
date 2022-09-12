from apscheduler.schedulers.background import BackgroundScheduler
from .views import scheduled_withdrawal,life_span_cheker,referal_scheduler
# from gentannieApp.views import referal_scheduler


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(veri_update, 'interval', seconds=10)
    scheduler.add_job(scheduled_withdrawal, 'interval', seconds=25)
    scheduler.add_job(life_span_cheker, 'interval', seconds=30)
    scheduler.add_job(referal_scheduler, 'interval', seconds=30)
    # scheduler.add_job(Due_checker, 'interval', seconds=10)
    scheduler.start()