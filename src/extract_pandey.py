import csv
P="Pandey_2012"; S="BHU Varanasi"
rows=[]
def add(trt,depth,var,val,unit,src,conf="text",cat="",note=""):
    rows.append([P,S,trt,depth,var,val,unit,src,conf,cat,note])
T4=["RCT-WCT","RNT-WCT","RCT-WNT","RNT-WNT"]
# a) site
for v,val,u,src in [("latitude",25.14,"deg N","p2 s2.1"),("longitude",82.03,"deg E","p2 s2.1"),
    ("elevation",76.19,"m asl","p2 s2.1"),("annual_rainfall_2009",462.0,"mm","p5 s3.2.1"),
    ("annual_rainfall_2010",771.9,"mm","p5 s3.2.1")]:
    add("all","",v,val,u,src,"text","a_site")
add("all","","site_name","Agricultural research farm, IAS, BHU, Varanasi","","p2 s2.1","text","a_site")
add("all","","climate","eastern Indo-Gangetic plains (no Koppen/temperature stats in text)","","p2 s2.1","text","a_site","daily weather only in Fig 2 (graph)")
add("all","","soil_class","Inceptisol","","p2 s2.1","text","a_site")
add("all","","texture_class","sandy loam","","p2 s2.1","text","a_site")
# b) initial soil 2003 (sampled 0-15 cm)
for v,val,u in [("pH",7.30,"-"),("bulk_density",1.43,"g/cm3"),("SOC",0.33,"%"),("total_N",0.32,"mg/g"),
    ("available_P",1.23,"mg/g"),("sand",58.49,"%"),("silt",15.21,"%"),("clay",26.30,"%")]:
    n=""
    if v in("total_N","available_P"): n="unit as printed (mg/g); magnitude suggests mg/kg - human review"
    add("initial_2003","0-15",v,val,u,"p3 Table 1","table","b_initial_soil",n)
# g) end soil 2009 per treatment
tab={"pH":([7.39,7.42,7.26,7.37],"-"),"bulk_density":([1.51,1.63,1.53,2.53],"g/cm3"),
 "SOC":([0.33,0.62,0.79,0.99],"%"),"total_N":([0.38,0.62,0.53,0.58],"mg/g"),
 "available_P":([1.05,1.43,1.46,1.87],"mg/g"),"sand":([62.62,64.61,67.19,60.47],"%"),
 "silt":([13.78,12.29,11.81,17.23],"%"),"clay":([23.60,23.10,21.00,22.30],"%")}
# Table 1 column order: RCT-WCT, RNT-WCT, RCT-WNT, RNT-WNT
for v,(vals,u) in tab.items():
    for t,x in zip(T4,vals):
        n="SOC method Walkley-Black; BD core 0-15 cm" if v in("SOC","bulk_density") else ""
        if v=="bulk_density" and t=="RNT-WNT": n="2.53 physically implausible (>2.65 particle density limit unreasonable for soil BD) - FLAG"
        add(t,"0-15",v,x,u,"p3 Table 1","table","g_end_soil",("year=2009; "+n).strip("; "))
# c) crops
for t in T4:
    add(t,"","rice_cultivar","PHB-71","","p2 s2.1","text","c_crop")
    add(t,"","wheat_cultivar","HD 2824","","p2 s2.1","text","c_crop")
for t in ["RNT-WCT","RNT-WNT"]:
    for y in(2009,2010): add(t,"","rice_sowing_date_direct_seeded",f"{y}-06-20","date","p3 s2.2","text","c_crop","zero-till drill")
for t in ["RCT-WCT","RCT-WNT"]:
    add(t,"","nursery_seeding_date","20 June (2009 and 2010)","date","p3 s2.2","text","c_crop")
    add(t,"","rice_transplanting_date","2009-07-16","date","p3 s2.2","text","c_crop")
    add(t,"","rice_transplanting_date","2010-07-19","date","p3 s2.2","text","c_crop")
for t in T4:
    add(t,"","rice_harvest_date","2009-10-30","date","p3 s2.2","text","c_crop")
    add(t,"","rice_harvest_date","2010-11-03","date","p3 s2.2","text","c_crop")
    add(t,"","rice_grain_yield","NA (only bar chart, no numbers)","kg/ha","p10 Fig 8","figure","c_crop","figure-only, low confidence; not extracted")
    add(t,"","straw_yield","NA (not reported)","kg/ha","-","missing","c_crop")
    add(t,"","wheat_sowing_harvest_dates","NA (not reported)","","-","missing","c_crop")
add("all","","experiment_period","2003-2010 (GHG measured 2009, 2010 rice season)","years","p2 s2.1","text","c_crop")
add("all","","plot_size","5.25 x 5.25","m","p2 s2.1","text","c_crop","3 replicates")
# d) tillage
til={"RCT-WCT":("puddling + repeated tillage + planking in standing water","disk plough + 2 harrowings by cultivator + planking"),
"RNT-WCT":("zero-till drill, no tillage","disk plough + 2 harrowings by cultivator + planking"),
"RCT-WNT":("puddling + repeated tillage + planking in standing water","zero-till drill, no tillage"),
"RNT-WNT":("zero-till drill, no tillage","zero-till drill, no tillage")}
for t,(r,w) in til.items():
    add(t,"","rice_tillage_operation",r,"","p2 s2.1","text","d_tillage","depth not given for rice")
    add(t,"","wheat_tillage_operation",w,"","p2 s2.1","text","d_tillage")
    if t.endswith("WCT"): add(t,"","wheat_tillage_depth",30,"cm","p2 s2.1","text","d_tillage","'approximately 30 cm'; machine = cultivator/disk plough")
for t in T4:
    add(t,"","tillage_timing","before sowing/transplanting of each crop (CT) or none (NT)","","p2 s2.1","text","d_tillage","calendar dates not given")
# e) fertiliser/residue
for t in T4:
    for v,x,u in [("N_total",150,"kg/ha"),("P2O5_total",75,"kg/ha"),("K2O_total",75,"kg/ha")]:
        add(t,"",v,x,u,"p3 s2.2","text","e_fertiliser","rice season")
    add(t,"","basal_fertiliser","15:15:15 NPK complex: all P and K + 50% of N (=75 kg N)","","p3 s2.2","text","e_fertiliser","at sowing/transplanting")
    add(t,"","topdress_urea_N",75,"kg N/ha","p3 s2.2","text","e_fertiliser","2 equal splits at tillering and panicle initiation; exact dates not given (arrows in Fig 4)")
    add(t,"","manure","none reported","","p3 s2.2","text","e_fertiliser")
    add(t,"","herbicide","pendimethalin 30EC 1 kg/ha (pre-emergence)" if t.startswith("RNT") else "butachlor 50EC 1.25 kg/ha (pre-emergence)","","p3 s2.2","text","e_fertiliser","+ one hand weeding at 25 DAS/DAT (p3) vs 30 DAS (p10): inconsistency")
    add(t,"","residue_after_harvest","20 cm standing straw retained; zero-till" if "NT" in t else "<5 cm stubble; mixed in by ploughing","","p2 s2.1","text","e_fertiliser","rice residue treatment, depends on previous crop tillage")
# f) irrigation
for t in T4:
    add(t,"","irrigation","NA: flooded to tillering then 'moderate moisture by rainfall or supplementary irrigation'; no dates/amounts","","p5 s3.2.1","missing","f_irrigation","DayCent needs schedule - human review")
w=csv.writer(open("/mnt/user-data/outputs/extracted_pandey.csv","w",newline="",encoding="utf-8-sig"))
w.writerow("paper_name,site,treatment,depth_cm,variable,value,unit,source,confidence,category,note".split(","))
w.writerows(rows); print(len(rows),"rows")
