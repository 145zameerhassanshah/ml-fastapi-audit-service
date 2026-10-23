from app.audit import fetch_recent_logs
from app.database import init_database

def main():
    init_database(); logs=fetch_recent_logs(20)
    if not logs:
        print('No audit records found.'); return
    print('Recent audit trail'); print('-'*100)
    for r in logs:
        print(f"ID={r['id']} | {r['timestamp_utc']} | status={r['status']} | class={r['predicted_class']} | prob={r['probability_class_1']} | error={r['error_message']}")

if __name__=='__main__': main()
