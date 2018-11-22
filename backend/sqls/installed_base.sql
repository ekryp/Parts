SELECT
	DATE_FORMAT(a.asset_installed_date, '%Y-%m-%d') as timestamp,
	a.asset_id_from_source as customer_asset_identifier,
	a.asset_serial_num as serial_number,
	a.asset_warranty_end_date as warranty_end_date,
	a.asset_service_end_date as service_end_date,
	a.asset_service_start_date as service_start_date,
	a.asset_partner_id as service_provider_id,
	a.asset_status_type_name as product_status_type,
	a.asset_status_type_date as product_status_date,
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
    a.asset_capacity_id as product_cassette_id,
	a.asset_capacity_count as product_cassette,
    pt.partner_name as service_provider_name,
	a.asset_firmware_id as firmware_id,
	a.asset_firmware_version_name as firmware_version_name,
    a.asset_firmware_release_date as firmware_version_release_date,
    a.asset_model_id as model_id,
	a.asset_model_name as model_name,
    
	ae.asset_ext_attr->>"$.asset_category_id" as product_category_id,
	ae.asset_ext_attr->>"$.asset_category_name" as product_category,
	ae.asset_ext_attr->>"$.asset_type_id" as product_type_id,
	ae.asset_ext_attr->>"$.asset_type_name" as product_type,
	ae.asset_ext_attr->>"$.asset_security_type_id" as product_lock_type_id,
	ae.asset_ext_attr->>"$.asset_security_type" as product_lock_type,
	ae.asset_ext_attr->>"$.asset_cd80_id" as product_cd80_id,
	ae.asset_ext_attr->>"$.asset_cd80" as product_cd80,
	ae.asset_ext_attr->>"$.asset_model_group_id" as model_group_id,
	ae.asset_ext_attr->>"$.asset_model_group_name" as model_group_name,
    ae.asset_ext_attr->>"$.asset_mw_name" as asset_middleware_name

FROM
	MYSQL_EKRYP_DB_NAME.asset as a
LEFT JOIN
	MYSQL_EKRYP_DB_NAME.site as si
ON
	site_id = a.asset_site_id
LEFT JOIN
	MYSQL_EKRYP_DB_NAME.end_customer as ec
ON
	si.site_end_cust_id = ec.end_cust_id
LEFT JOIN
	MYSQL_EKRYP_DB_NAME.asset_extended as ae
ON
	ae.asset_id = a.asset_id
LEFT JOIN
	MYSQL_EKRYP_DB_NAME.partner as pt
ON
	pt.partner_id = a.asset_partner_id
where a.cust_id = prospect_id
	;
