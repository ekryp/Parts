SELECT
	DATE_FORMAT(ad.dailywork_date, '%Y-%m-%d') as timestamp,
	ad.asset_id as asset_id,
	ad.work_units as daily_work
FROM
	MYSQL_EKRYP_DB_NAME.dailywork as ad
WHERE
	ad.dailywork_date IS NOT NULL
AND
	ad.work_type='notes_in'
	;
