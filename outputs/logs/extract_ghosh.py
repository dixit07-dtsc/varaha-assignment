import csv
P="Ghosh_2017"; S="ICAR-IIPR Kanpur"
rows=[]
def add(trt,depth,var,val,unit,src,conf="text",cat="",note=""):
    rows.append([P,S,trt,depth,var,val,unit,src,conf,cat,note])
# NOTE: 'pN' = PDF page number (journal page = N+428)
# a) site
add("all","","site_name","ICAR-Indian Institute of Pulses Research (IIPR) main research farm, Kalyanpur, Kanpur","","p2 s2.1","text","a_site")
add("all","","latitude",round(26+27/60,4),"deg N","p2 s2.1","text","a_site","printed 26deg27'N; converted from deg-min")
add("all","","longitude",round(80+14/60,4),"deg E","p2 s2.1","text","a_site","printed 80deg14'E; converted from deg-min")
add("all","","elevation",152.4,"m asl","p2 s2.1","text","a_site")
add("all","","climate","sub-humid tropical","","p2 s2.1","text","a_site")
add("all","","annual_rainfall",722,"mm","p2 s2.1","text","a_site")
add("all","","Tmax_mean_annual",33.0,"C","p2 s2.1","text","a_site")
add("all","","Tmin_mean_annual",20.0,"C","p2 s2.1","text","a_site")
add("all","","soil_class","Typic Ustochrept (Inceptisol)","","p2 s2.1","text","a_site")
add("all","","texture_class","sandy loam","","p2 s2.1","text","a_site")
add("all","","experiment_start","2003-07 (rainy season)","","p2 s2.2","text","a_site","sampling after 8 yrs (2003-2011)")
# b) initial soil
add("initial","","SOC",2.8,"g/kg","p2 s2.1","text","b_initial_soil","depth not stated; same for upland and lowland")
for v in ["sand","silt","clay","bulk_density","pH","field_capacity","wilting_point","sat_hydraulic_conductivity"]:
    add("initial","",v,"NA (not reported)","","-","missing","b_initial_soil")
# g) end soil: Tables 3 (lowland), 4 (upland)
fr=["Cfrac1","Cfrac2","Cfrac3","Cfrac4","TOC"]
T3={"0-20":{"L_RW":[3.59,2.98,5.48,5.24,17.29],"L_RWRC":[4.85,3.41,5.37,4.79,18.42],"L_CT":[3.58,2.53,5.14,4.83,16.08],"L_RDF":[4.33,3.46,5.32,4.98,18.09],"L_ORG":[4.94,3.60,5.79,5.24,19.57]},
"20-40":{"L_RW":[3.89,3.05,4.86,2.93,14.73],"L_RWRC":[4.08,3.05,4.55,2.79,14.47],"L_CT":[3.07,2.81,4.62,2.88,13.38],"L_RDF":[4.75,3.22,4.62,2.91,15.50],"L_ORG":[5.14,3.12,4.68,2.8,15.74]},
"40-60":{"L_RW":[1.53,1.5,1.43,1.88,6.34],"L_RWRC":[1.45,1.49,1.54,1.82,6.30],"L_CT":[1.54,1.55,1.44,1.76,6.29],"L_RDF":[1.55,1.45,1.47,1.86,6.33],"L_ORG":[1.38,1.49,1.55,2.01,6.43]}}
T4={"0-20":{"U_MW":[5.37,3.09,2.78,3.45,14.69],"U_MWMC":[6.32,3.49,3.09,3.77,16.67],"U_CT":[4.36,2.97,2.64,3.35,13.32],"U_RDF":[6.18,3.27,2.97,3.57,15.99],"U_ORG":[6.98,3.63,3.21,3.91,17.73]},
"20-40":{"U_MW":[3.61,1.4,3.37,2.8,11.18],"U_MWMC":[3.55,1.54,2.84,2.85,10.78],"U_CT":[3.28,1.32,2.94,2.88,10.42],"U_RDF":[3.59,1.69,3.18,2.71,11.17],"U_ORG":[3.88,1.56,3.19,2.9,11.53]},
"40-60":{"U_MW":[1.65,1.88,1.02,1.50,6.05],"U_MWMC":[1.54,2.08,0.99,1.52,6.13],"U_CT":[1.59,1.43,0.89,1.39,5.3],"U_RDF":[1.49,2.34,1.1,1.44,6.37],"U_ORG":[1.70,2.18,1.03,1.69,6.6]}}
mn="year~2011 (after 8 yr); marginal mean (cropping system averaged over nutrient mgmt, or nutrient mgmt averaged over systems), NOT full factorial; TOC = Walkley-Black C x 1.33"
for tab,pg in((T3,"p5 Table 3"),(T4,"p6 Table 4")):
    for d,tr in tab.items():
        for t,vals in tr.items():
            for v,x in zip(fr,vals): add(t,d,v,x,"g/kg",pg,"table","g_end_soil",mn)
LI={"L_RW":([1.28,1.54,1.69],[105.6,111.1,77.9]),"L_RWRC":([1.46,1.58,1.68],[126.0,110.8,135.9]),"L_CT":([1.30,1.51,1.69],[100.0]*3),"L_RDF":([1.40,1.65,1.66],[120.5,122.8,112.6]),"L_ORG":([1.40,1.52,1.71],[126.9,110.0,108.1]),
"U_MW":([1.70,1.52,1.63],[120.7,109.1,111.3]),"U_MWMC":([1.70,1.55,1.67],[126.1,105.5,112.0]),"U_CT":([1.59,1.47,1.43],[100.0]*3),"U_RDF":([1.75,1.62,1.95],[127.7,112.5,117.2]),"U_ORG":([1.77,1.52,1.56],[142.4,109.3,117.8])}
for t,(li,cmi) in LI.items():
    for d,a,b in zip(["0-20","20-40","40-60"],li,cmi):
        add(t,d,"lability_index",a,"-","p7 Table 5","table","g_end_soil_derived","derived index, not a DayCent input")
        add(t,d,"carbon_management_index",b,"-","p7 Table 5","table","g_end_soil_derived","derived index, not a DayCent input")
for t in LI:
    for v in ["bulk_density","POC"]:
        pass
add("all","0-20","POC","NA (bar chart only, Fig 1)","g/kg","p6 Fig 1","figure","g_end_soil","figure-only; not extracted")
add("all","","end_bulk_density","NA (not reported)","","-","missing","g_end_soil","needed for SOC stock (g/kg -> Mg/ha)")
add("all","","sampling_depths_text","0-20, 20-40, 40-60, 60-80 cm (4 depths)","cm","p3 s2.3","text","g_end_soil","tables show only 3 depths (to 60 cm) - inconsistency")
add("all","","SOC_method","Walkley-Black wet oxidation; TOC = oxidizable C x 1.33","","p3 s2.3","text","g_end_soil","post-hole auger, 4 spots/plot, after harvest of last crop")
# c) crops (Table 1 p3)
sysd={"lowland":"RW (rice-wheat); RWRC (rice-wheat-rice-chickpea)","upland":"MW (maize-wheat); MWMC (maize-wheat-maize-chickpea)"}
for k,v in sysd.items(): add(k,"","rotation_sequence",v,"","p2 s2.2","text","c_crop","chickpea included alternate years")
crops=[("lowland","rice","Pant Dhan 12","40","20x20 cm","June wk2 - Oct wk4","120-60-40","1/3 N+P+K basal; 1/3 N at 25 DAT; 1/3 N at 45 DAT","8-10"),
("lowland","wheat","PBW 343","100","22.5 cm continuous","Nov wk3 - Mar wk3","120-60-40","1/3 N+P+K basal; 1/3 N at 21 DAS; 1/3 N at 45 DAS","5"),
("lowland","chickpea","KWR 108","70","30x10 cm","Apr wk1 - Jun wk1","20-60-40","N+P+K all basal","2"),
("upland","maize","Azad Uttam","18-20","50x20 cm","June wk3 - Oct wk3","120-60-40","1/3 N+P+K basal; 1/3 N at 25 DAS; 1/3 N at 45 DAS","2"),
("upland","wheat","PBW 343","100","22.5 cm continuous","Nov wk3 - Mar wk3","120-60-40","1/3 N+P+K basal; 1/3 N at 21 DAS; 1/3 N at 45 DAS","5"),
("upland","chickpea","DCP-92-3","70","30x10 cm","Apr wk1 - Jun wk1","20-60-40","N+P+K all basal","2")]
for sy,c,cv,sr,sp,se,npk,tm,ir in crops:
    t=f"{sy}_{c}"
    add(t,"","cultivar",cv,"","p3 Table 1","table","c_crop")
    add(t,"","seed_rate",sr,"kg/ha","p3 Table 1","table","c_crop")
    add(t,"","spacing",sp,"","p3 Table 1","table","c_crop","PDF text '20 9 20' read as 20x20 (x garbled)")
    add(t,"","crop_season_seed_to_seed",se,"month(week)","p3 Table 1","table","c_crop","only month+week, no exact sowing/harvest dates"+("; chickpea Apr-Jun implausible for a winter crop - FLAG" if c=="chickpea" else ""))
    add(t,"","NPK_rate",npk,"kg/ha (N-P-K)","p3 Table 1","table","e_fertiliser","P and K oxide basis not stated")
    add(t,"","fertiliser_timing",tm,"","p3 Table 1","table","e_fertiliser","DAT/DAS only, no calendar dates")
    add(t,"","n_irrigations",ir,"count/season","p3 Table 1","table","f_irrigation","need-based, mean of 4 yrs; no dates, depth or method")
    add(t,"","grain_yield","NA (only % increase in Fig 4)","kg/ha","p10 Fig 4","figure","c_crop","figure-only")
    add(t,"","straw_yield","NA (not reported)","kg/ha","-","missing","c_crop")
# d) tillage
add("all","","tillage","NA (machine, depth and timing not reported)","","-","missing","d_tillage","only crop-residue chopping by rotary machine mentioned")
# e) fertiliser / organics
for v,x,u in [("FYM_rate",5,"Mg/ha"),("FYM_N",28,"kg/ha"),("FYM_P",9,"kg/ha"),("FYM_K",26,"kg/ha"),("FYM_C",448,"kg/ha")]:
    add("ORG","",v,x,u,"p3 s2.2","text","e_fertiliser","applied before rainy-season crops; per application (per year assumed) - human review" if v=="FYM_C" else "applied before rainy-season crops")
add("ORG","","residue_management","all crop residue chopped by rotary machine, spread and mixed in before next crop","","p3 s2.2","text","e_fertiliser","amount (t/ha) only as C in Table 2")
add("ORG","","biofertiliser","Azotobacter (cereals), Rhizobium (pulses), PSB; 20 g/kg seed","","p3 s2.2","text","e_fertiliser")
add("RDF","","S_gypsum",20,"kg S/ha","p2-3 s2.2","text","e_fertiliser")
add("RDF","","Zn_as_ZnSO4",25,"kg/ha","p2-3 s2.2","text","e_fertiliser")
add("RDF","","B_as_borax",10,"kg/ha","p3 s2.2","text","e_fertiliser")
add("RDF","","N_P_K_sources","urea, DAP, muriate of potash","","p2 s2.2","text","e_fertiliser")
add("CT","","fertiliser","none (control)","","p2 s2.2","text","e_fertiliser")
# Table 2
T2={"L_RW":{"RDF":[240.0,52.4,43.7,20.0,4.2],"ORG":[103.6,25.9,142.5,24.4,0.29,6.5,36.8,43.3]},
"L_RWRC":{"RDF":[190.0,52.4,43.7,20.0,4.2],"ORG":[107.0,26.8,146.0,28.2,0.40,6.5,43.0,49.5]},
"U_MW":{"RDF":[240,52.4,43.7,20,4.20],"ORG":[91.6,18.9,122.3,10.8,0.42,6.5,36.2,42.7]},
"U_MWMC":{"RDF":[190,52.4,43.7,20,4.20],"ORG":[109.9,22.3,142.5,16.1,0.50,6.5,43.8,50.31]}}
for sy,d in T2.items():
    for nm,vals in d.items():
        for v,x in zip(["annual_N","annual_P","annual_K","annual_S","annual_Zn"],vals[:5]):
            add(f"{sy}_{nm}","",v,x,"kg/ha/yr","p4 Table 2","table","e_fertiliser","mean of last 2 yrs (2009-11)")
        if len(vals)>5:
            for v,x in zip(["cumC_FYM","cumC_residue","cumC_total"],vals[5:]):
                add(f"{sy}_{nm}","",v,x,"Mg C/ha","p4 Table 2","table","e_fertiliser","cumulative 8 yrs"+("; 50.31 has 2 decimals, likely typo for 50.3" if x==50.31 else ""))
    add(f"{sy}_CT","","annual_nutrient_input","none (dash in table)","","p4 Table 2","table","e_fertiliser")
# f) irrigation
add("all","","irrigation_method_dates_amounts","NA (not reported; wheat 'assured irrigated' only)","","-","missing","f_irrigation")
w=csv.writer(open("/mnt/user-data/outputs/extracted_ghosh.csv","w",newline="",encoding="utf-8-sig"))
w.writerow("paper_name,site,treatment,depth_cm,variable,value,unit,source,confidence,category,note".split(","))
w.writerows(rows); print(len(rows),"rows")
# quick self-check: Cfrac1-4 sum = TOC
bad=0
for tab in(T3,T4):
    for d,tr in tab.items():
        for t,v in tr.items():
            if abs(sum(v[:4])-v[4])>0.015: bad+=1; print("sum mismatch",t,d,sum(v[:4]),v[4])
print("sum mismatches:",bad)
