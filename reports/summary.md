Week 2 Update: What’s going on with our data?
Key findings
The Pipeline is Live: I've got the ETL fully automated. It’s taking the raw CSVs, cleaning them up, and spitting out a final analytics_table.parquet.

Perfect Match: Good news on the data quality—every single one of the 100 orders we processed found its user in the system (1.0 match rate). No "ghost" orders this time!

User Activity: We have 104 users on file, but only 100 orders came through. This means a few users haven't pulled the trigger on a purchase yet, or they're just lurking.

Cleanup Worked: We handled the messy statuses (like "refunded" vs "Refund") and flagged the crazy high-dollar outliers so they don't mess up our averages.

How I’m defining things
Revenue: I'm summing up the amount column, but I created an amount_is_outlier flag. You should probably filter those out if you want to see "normal" sales.

Refunds: I normalized the status codes. If it says "refund" in status_clean, it's a refund—no matter how messy it looked in the raw data.

Time Tracking: I broke the timestamps down into year, month, and day of the week so we can see when people are actually buying stuff.

The "Dirty" Data (Caveats)
Coverage: Right now, the join is perfect (1.0). If this drops in the future, it means we’re losing track of which countries our money is coming from.

Timestamps: We didn't have any missing dates in this run, but the code is now set up to catch them if the raw data starts getting flaky.

Outliers: I used Winsorization. Basically, I "clipped" the extreme 1% of values to keep the charts from looking insane.

What’s next?
Who are the 4 users? I want to look into the 4 users who haven't ordered anything. Are they new signups, or did they get stuck at checkout?

Country deep-dive: Now that the analytics_table is ready, we should see which country is actually our "MVP" for revenue.

Growth: I want to use those month/year columns to see if we’re actually growing or just staying flat.