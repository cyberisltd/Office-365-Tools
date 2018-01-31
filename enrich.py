#!/usr/bin/python3
import csv, sys, json
import geoip2.database

filename = sys.argv[1]
outfile = open(sys.argv[2],'w',newline='')

geoip = geoip2.database.Reader('GeoLite2-Country_20180102/GeoLite2-Country.mmdb')

fieldnames = ['CreationDate','UserIds','Operations','IP','Country','UA','UserAuthenticationMethod','AuditData' ]
writer = csv.DictWriter(outfile,fieldnames=fieldnames,extrasaction='ignore')
writer.writeheader()

with open(filename, newline='') as f:
    reader = csv.DictReader(f)
    try:
        for row in reader:
            try:
                audit = json.loads(row['AuditData'])
            except json.JSONDecodeError:
                print("ERROR")
                continue

            try:
                ip = audit['ClientIP']
                row['IP'] = ip

            except KeyError:
                pass 

            try:
                response = geoip.country(ip)
                row['Country'] = response.country.name
            except (geoip2.errors.AddressNotFoundError,ValueError):
                pass

            try: 
                extendedprops = audit['ExtendedProperties']
                for prop in extendedprops:
                    if prop['Name'] == "UserAgent": 
                        row['UA'] = prop['Value']
                    if prop['Name'] == 'UserAuthenticationMethod':
                        row['UserAuthenticationMethod'] = prop['Value']
            except KeyError:
                pass
            
            writer.writerow(row)


    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
