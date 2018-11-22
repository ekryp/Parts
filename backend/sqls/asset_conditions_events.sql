SELECT
        DATE_FORMAT(ace.event_date, '%Y-%m-%d') as timestamp,
        a.asset_id_from_source as customer_asset_identifier,
        a.asset_serial_num as serial_number,
        ace.event_date as event_date,
        ace.event_time as event_time,
        ace.event_code_id as code_id,
        ace.event_code_value as code,
        ace.event_code_type_id as code_type,
        ace.event_code_criticality as criticality,
        ace.event_code_desc as description
FROM
        MYSQL_EKRYP_DB_NAME.asset_event as ace
LEFT JOIN
        MYSQL_EKRYP_DB_NAME.asset as a
ON
        ace.asset_id = a.asset_id
WHERE
        ace.event_date IS NOT NULL
		and ace.cust_id = prospect_id
        ;
