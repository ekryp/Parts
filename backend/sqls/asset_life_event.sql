SELECT 
	DATE_FORMAT(ale.asset_life_event_date, '%Y-%m-%d') as timestamp,
	ale.asset_id_from_source as customer_asset_identifier,
	aii.asset_serial_num as serial_number,
	ale.asset_life_event_type_id as life_event_code,
	ale.asset_life_event_date as event_date,
	ale.asset_life_event_type_value as life_event_value,
	ale.asset_life_event_type_value_desc as life_event_description
FROM
	MYSQL_EKRYP_DB_NAME.asset_life_event as ale
LEFT JOIN
	MYSQL_EKRYP_DB_NAME.asset aii
ON
	ale.asset_id=aii.asset_id
WHERE
	ale.asset_life_event_date IS NOT NULL
	AND YEAR(ale.asset_life_event_date) > 2000
	;

