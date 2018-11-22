SELECT 
	DATE_FORMAT(inc.incident_date,'%Y-%m-%d') AS timestamp,
	inc.incident_id_from_source as sr_id,
	inc.incident_status as status,
	inc.cust_source_sys_ref as service_request_id,
	inc.incident_category as incident_category,
	a.asset_id_from_source as customer_asset_identifier,
	a.asset_serial_num as serial_number,
	a.asset_installed_date as installed_date,
	a.asset_status_type_name as product_status_type,
	inc.incident_priority as priority,
	inc.incident_initial_reason as initial_reason,
	inc.incident_final_reason as final_reason,
	si.site_name as site_name,
	si.site_city as city,
	si.site_state as state,
	si.site_country as country,
	si.site_tz as tzinfo,
	si.site_lat as site_latitude,
	si.site_lon as site_longitude,
	si.site_id as site_id_mapped,
	si.site_geo as geo,
	ec.end_cust_name as company_name,
	ec.end_cust_id as company_id_mapped,
	pt.partner_name as service_provider_name,
	a.asset_firmware_version_name as firmware_name,
	a.asset_firmware_release_date as firmware_version_release_date,
    a.asset_capacity_count as product_cassette,
    a.asset_model_name as model_name,
    
    sie.site_ext_attr->>"$.site_pm_days" as site_pm_days,
	sie.site_ext_attr->>"$.site_pm_work" as site_pm_notes,
    
    ae.asset_ext_attr->>"$.asset_category_name" as product_category,
	ae.asset_ext_attr->>"$.asset_type_name" as product_type,
	ae.asset_ext_attr->>"$.asset_security_type" as product_lock_type,
	ae.asset_ext_attr->>"$.asset_cd80" as product_cd80,
	ae.asset_ext_attr->>"$.asset_model_group_name" as model_group,
	CASE
	WHEN(DATEDIFF(inc.incident_date, a.asset_installed_date) >= 0) THEN DATEDIFF(inc.incident_date, a.asset_installed_date)
	ELSE 0
	END as days,
	(SELECT 
		sum(work_units) 
	from 
		MYSQL_EKRYP_DB_NAME.dailywork
	where 
		asset_id = inc.asset_id
	AND
		dailywork_date BETWEEN a.asset_installed_date and inc.incident_date)
	as notes_processed,
	inc.incident_in_warranty as in_warranty,
	inc.intervention_type as intervention_type
FROM
	MYSQL_EKRYP_DB_NAME.incident as inc

LEFT JOIN
	MYSQL_EKRYP_DB_NAME.asset as a
ON
	inc.asset_id = a.asset_id
LEFT JOIN
	MYSQL_EKRYP_DB_NAME.asset_extended as ae
ON
	ae.asset_id = a.asset_id
LEFT JOIN
	MYSQL_EKRYP_DB_NAME.site as si
ON
	a.asset_site_id = si.site_id
LEFT JOIN
	MYSQL_EKRYP_DB_NAME.site_extended sie
ON
	si.site_id=sie.site_id
LEFT JOIN
	MYSQL_EKRYP_DB_NAME.partner as pt
ON
	pt.partner_id = a.asset_partner_id
LEFT JOIN
	MYSQL_EKRYP_DB_NAME.end_customer as ec
ON
	si.site_end_cust_id = ec.end_cust_id
where inc.cust_id = prospect_id	
	;