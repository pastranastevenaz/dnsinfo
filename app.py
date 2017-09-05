import os
import requests
import sys
import json
from flask import Flask, request, render_template, url_for, flash, session, redirect
from timeit import default_timer as timer

app=Flask(__name__)
app.secret_key = "secret_key"

@app.route("/")
def index():
    return render_template('index.html')
        # return "?This is the post"
    # elif request.method == 'GET':


@app.route("/dnsshow", methods=['GET', 'POST'])
def dnsshow():
    domain_suffix = request.form['domain']
    if request.method == 'POST':
        # IF Domain is empty
        if not domain_suffix:
            flash("PLease enter a domain")
            return redirect(url_for('index'))
        try:
            start = timer()
            # EMPTY LISTS
            all_a_records=[]
            all_aaaa_records=[]
            all_mx_records=[]
            all_cn_records=[]
            all_soa_records=[]
            all_txt_records=[]
            all_ns_records=[]
            # DOMAIN PREFIXES
            a_domain_prefix='http://dns-api.org/A/'
            aaaa_domain_prefix='http://dns-api.org/AAAA/'
            mx_domain_prefix='http://dns-api.org/MX/'
            cn_domain_prefix='http://dns-api.org/CNAME/'
            soa_domain_prefix='http://dns-api.org/SOA/'
            txt_domain_prefix='http://dns-api.org/TXT/'
            ns_domain_prefix='http://dns-api.org/NS/'
            # @ RECORD LOOKUP
            domain_to_lookup = a_domain_prefix+domain_suffix
            response = requests.get(domain_to_lookup)
            for a in response.json():
                all_a_records.append(a)
                print('finished first lookup')
            # AAAA RECORD LOOKUP
            domain_to_lookup = aaaa_domain_prefix+domain_suffix
            response = requests.get(domain_to_lookup)
            for aaaa in response.json():
                all_aaaa_records.append(aaaa)
                print('finished second lookup')
            # MX RECORD LOOKUP
            domain_to_lookup=mx_domain_prefix+domain_suffix
            response=requests.get(domain_to_lookup)
            print("finished the 3rd lookup")
            for mx in response.json():
                all_mx_records.append(mx)
            # =================================
            # CNAME RECORD LOOKUP
            domain_to_lookup=cn_domain_prefix+domain_suffix
            response=requests.get(domain_to_lookup)
            print("finished the 4th lookup")
            for cn in response.json():
                all_cn_records.append(cn)
            # =================================
            # SOA RECORD LOOKUP
            domain_to_lookup=soa_domain_prefix+domain_suffix
            response=requests.get(domain_to_lookup)
            print("finished the 5th lookup")
            for soa in response.json():
                all_soa_records.append(soa)
            # =================================
            # TXT RECORD LOOKUP
            domain_to_lookup=txt_domain_prefix+domain_suffix
            response=requests.get(domain_to_lookup)
            print("finished the sixth lookup")
            for txt in response.json():
                all_txt_records.append(txt)
            # =================================
            # NAMESERVER RECORD LOOKUP
            domain_to_lookup=ns_domain_prefix+domain_suffix
            response=requests.get(domain_to_lookup)
            print("finished the 7th lookup")
            for ns in response.json():
                all_ns_records.append(ns)
            end=timer()
            print(str(end)+" - "+str(start)+" = " +str(end-start))
            return render_template('index.html',
                domain = domain_suffix.upper(),
                all_a_records = all_a_records,
                all_aaaa_records = all_aaaa_records,
                all_mx_records = all_mx_records,
                all_cn_records = all_cn_records,
                all_soa_records = all_soa_records,
                all_txt_records = all_txt_records,
                all_ns_records = all_ns_records)
        except:
            e = sys.exc_info()[0]
            print(str(e))
            return redirect(url_for(index))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run(host='0.0.0.0', port=port, debug=True)
