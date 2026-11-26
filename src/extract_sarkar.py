import csv, sys, os
# 'pN' = PDF page number (journal page = N+261)
P = "Sarkar_2011"; S = "IIT Kharagpur experimental farm"
OUT = sys.argv[1] if len(sys.argv) > 1 else r"outputs\excel\extracted_sarkar.csv"
rows = []
def add(trt, depth, var, val, unit, src, conf="text", cat="", note=""):
    rows.append([P, S, trt, depth, var, val, unit, src, conf, cat, note])

# ---- a) site (p4) ----
a = "a_site"
add("all","","site_name","Experimental farm, Agri & Food Engg Dept, IIT Kharagpur, West Bengal","","p4 Experimental Site","text",a)
add("all","","latitude",round(22+19/60,4),"deg N","p4 Experimental Site","text",a,"printed 22deg19'N; converted")
add("all","","longitude",round(87+19/60,4),"deg E","p4 Experimental Site","text",a,"printed 87deg19'E; converted")
add("all","","elevation",48,"m asl","p4 Experimental Site","text",a)
add("all","","climate","sub-humid subtropical","","p4 Experimental Site","text",a)
add("all","","annual_rainfall",1200,"mm","p4 Experimental Site","text",a,"70-75% in Jun-Oct")
add("all","","temp_range_mean","21-32","C","p4 Experimental Site","text",a)
add("all","","temp_max_extreme",47,"C","p4 Experimental Site","text",a,"Apr-May")
add("all","","soil_class","Haplustalf (acid lateritic sandy loam)","","p4 Experimental Site","text",a)
add("all","","experiment_period","2001-2003 (Jun 2001 - Oct 2003)","","p4 Details of Field Experiment","text",a)
add("all","","basic_infiltration_rate",6.0,"mm/hr","p4 Experimental Site","text",a)

# ---- b) initial soil, Table 1 (p5) ----
b = "b_initial_soil"
T1 = {  # var: (unit, [0-15, 15-30, 30-45])
 "pH": ("-", [5.5,5.6,5.8]), "SOC": ("%", [0.36,0.32,0.22]),
 "clay": ("%", [14.3,21.0,27.3]), "silt": ("%", [26.2,19.3,20.2]), "sand": ("%", [59.5,59.7,52.5]),
 "bulk_density": ("Mg/m3", [1.62,1.56,1.59]),
 "sat_hydraulic_conductivity": ("cm/day", [9.82,6.74,0.91]),
 "CEC": ("cmol/kg", [8.1,9.2,9.6]), "total_N": ("g/kg", [0.04,0.05,0.06])}
depths = ["0-15","15-30","30-45"]
for v,(u,vals) in T1.items():
    for d,x in zip(depths,vals):
        n = "unit printed 'Mg/m'; assumed Mg/m3" if v=="bulk_density" else ""
        add("initial",d,v,x,u,"p5 Table 1","table",b,n)
for d,x,s in zip(["0-15","15-30","30-45"],[9.8,12.9,14.0],["2.54","7.62","12.7"]):
    add("initial",d,"soil_strength",x,"kg/cm2","p5 Table 1","table",b,f"measured at {s} cm depth")
for v in ["field_capacity","wilting_point"]:
    add("initial","",v,"NA (not reported)","-","-","missing",b,"estimate with Saxton-Rawls (assumption)")

# ---- c) crops (p4,p6) ----
c = "c_crops"
add("all","","crop_sequence","TR-W-F and DR-W-F (rice-wheat-fallow)","","p5-p6","text",c)
add("all","","rice_cultivar","IR36","","p4 Details of Field Experiment","text",c)
add("all","","wheat_cultivar","Sonalika","","p4 Details of Field Experiment","text",c)
for y in [2001,2002,2003]:
    add("all","","rice_season",f"Jun-Oct {y} (monsoon)","","p4 Details of Field Experiment","text",c,"exact sowing/harvest dates not given")
for y in ["2001-02","2002-03"]:
    add("all","","wheat_season",f"Nov-Apr {y}","","p4 Details of Field Experiment","text",c,"exact sowing/harvest dates not given")
add("TR","","seedling_age",21,"days","p5","text",c,"nursery seedlings transplanted in hills")
add("DR","","row_spacing",20,"cm","p5","text",c)
add("all","","straw_yield","NA (not reported)","-","-","missing",c)
# yields
def y(trt,var,val,yr,src): add(trt,"",var,val,"kg/ha",src,"table","c_crops",f"year {yr}; marginal mean, not full factorial")
t6a={"T1":[3983,4069,4422],"T2":[3914,3871,4261]}
for t,v in t6a.items():
    for yr,x in zip([2001,2002,2003],v): y(f"{t} (TR)","grain_yield_rice",x,yr,"p22 Table 6a")
for r,v in {"r0w0":[3778,4162],"r0w1":[4038,4401],"r1w0":[3919,4253],"r1w1":[4146,4549]}.items():
    for yr,x in zip([2002,2003],v): y(f"{r} (TR)","grain_yield_rice",x,yr,"p22 Table 6a")
for t,v in {"T3":[2022,2128,2273],"T4":[1688,1455,1443]}.items():
    for yr,x in zip([2001,2002,2003],v): y(f"{t} (DR)","grain_yield_rice",x,yr,"p22 Table 6b")
for r,v in {"r0w0":[1496,1676],"r0w1":[1839,1882],"r1w0":[1770,1799],"r1w1":[2061,2075]}.items():
    for yr,x in zip([2002,2003],v): y(f"{r} (DR)","grain_yield_rice",x,yr,"p22 Table 6b")
w7={"T1_t0":[1450,1383],"T1_t1":[1698,1592],"T2_t0":[1353,1366],"T2_t1":[1554,1543]}
w8={"T3_t0":[1705,1680],"T3_t1":[1885,1932],"T4_t0":[1556,1589],"T4_t1":[1779,1696]}
for tab,d,src,sys_ in [(7,w7,"p23 Table 7","TR"),(8,w8,"p24 Table 8","DR")]:
    for t,v in d.items():
        for yr,x in zip(["2001-02","2002-03"],v): y(f"{t} (wheat after {sys_})","grain_yield_wheat",x,yr,src)
for sys_,src,r1,r2 in [("TR","p23 Table 7",{"r0":1398,"r1":1629},{"r0w0":1419,"r0w1":1456,"r1w0":1481,"r1w1":1527}),
                       ("DR","p24 Table 8",{"r0":1670,"r1":1793},{"r0w0":1679,"r0w1":1709,"r1w0":1721,"r1w1":1788})]:
    for r,x in r1.items(): y(f"{r} (wheat after {sys_})","grain_yield_wheat",x,"2001-02",src)
    for r,x in r2.items(): y(f"{r} (wheat after {sys_})","grain_yield_wheat",x,"2002-03",src)

# ---- d) tillage (p5-p6) ----
d_ = "d_tillage"
til = [("T1 (TR)","rotavator puddling (intensive wet)","rice","June (onset of monsoon)","NA"),
       ("T2 (TR)","power tiller puddling (less intensive wet)","rice","June (onset of monsoon)","NA"),
       ("T3 (DR)","tractor cultivator + disc harrow (intensive dry)","rice","June (onset of monsoon)",15),
       ("T4 (DR)","tractor cultivator (less intensive dry)","rice","June (onset of monsoon)",7.5),
       ("t1 (wheat)","cultivator + disc harrow","wheat","November",15),
       ("t0 (wheat)","cultivator","wheat","November",7.5)]
for t,m,cr,tm,dp in til:
    add(t,"","tillage_machine",m,"","p5-p6 Details of Field Experiment","text",d_)
    add(t,"","tillage_timing",tm,"","p5-p6 Details of Field Experiment","text",d_)
    add(t,"","tillage_depth",dp,"cm","p5-p6 Details of Field Experiment","text" if dp!="NA" else "missing",d_,"puddling depth not stated" if dp=="NA" else "")

# ---- e) fertiliser and organic (p6) ----
e = "e_fertiliser_organic"
for cr in ["rice","wheat"]:
    add(f"all ({cr})","","P2O5",50,"kg/ha","p6","text",e,"single super phosphate, after tillage, each crop")
    add(f"all ({cr})","","K2O",50,"kg/ha","p6","text",e,"muriate of potash, after tillage, each crop")
for n in [0,40,60,80,100,120]:
    add(f"N{n}","","N_rate",n,"kg/ha","p6","text",e,"urea, two equal splits; rice: active tillering+booting; wheat: CRI+panicle initiation")
for r,(ri,wh) in {"r0w0":(0,0),"r0w1":(0,4),"r1w0":(4,0),"r1w1":(4,4)}.items():
    add(r,"","rice_straw_to_wheat",ri,"t/ha","p6","text",e,"chopped, incorporated at land prep (from Nov 2002); retained")
    add(r,"","wheat_straw_to_rice",wh,"t/ha","p6","text",e,"chopped, incorporated at land prep (from 2002); retained")
add("all","","manure","NA (not reported)","-","-","missing",e)
add("all","","fertiliser_dates","NA (only stage given)","-","-","missing",e,"month/day not stated")

# ---- f) irrigation (p6) ----
f = "f_irrigation"
add("wheat","","irrigation_amount",6,"cm per irrigation","p6","text",f,"scheduled at IW/CPE = 1.0")
add("wheat","","irrigation_dates","NA (not reported)","-","-","missing",f)
add("rice","","irrigation","rainfed / not reported","-","p5, p23 ('rainfed')","text",f,"no irrigation amounts reported")
add("wheat","","irrigation_method","NA (not reported)","-","-","missing",f)

# ---- g) end-of-experiment soil ----
g = "g_end_soil"
t2 = {"TR":{"T1":3.41,"T2":3.57,"r0w0":3.14,"r0w1":3.63,"r1w0":3.51,"r1w1":3.67,
            "N0":3.16,"N40":3.20,"N60":3.40,"N80":3.48,"N100":3.78,"N120":3.92},
      "DR":{"T3":3.90,"T4":3.96,"r0w0":3.28,"r0w1":4.17,"r1w0":4.00,"r1w1":4.27,
            "N0":3.70,"N40":3.79,"N60":3.87,"N80":3.98,"N100":4.08,"N120":4.16}}
for s_,dd in t2.items():
    for t,x in dd.items():
        add(f"{t} ({s_})","depth not stated","SOC_end",x,"g/kg","p10 Table 2","table",g,
            "Oct 2003; modified Walkley-Black; marginal mean; depth not stated (methods list 0-15,15-30,30-45)")
# BD / Ksat Tables 3,4
def bk(tab,src,sysname,data):
    for (til_,res),(bd,ks) in data.items():
        for d,b_,k_ in zip(depths,bd,ks):
            add(f"{til_}_{res} ({sysname})",d,"bulk_density_end",b_,"Mg/m3",src,"table",g,f"after {sysname} harvest 2003")
            add(f"{til_}_{res} ({sysname})",d,"sat_hydraulic_conductivity_end",k_,"cm/day",src,"table",g,f"after {sysname} harvest 2003")
bk(3,"p14 Table 3","TR",{("T1","r0w0"):([1.69,1.73,1.75],[7.81,6.68,1.28]),("T1","r0w1"):([1.66,1.72,1.72],[7.85,6.70,1.26]),
 ("T1","r1w0"):([1.65,1.71,1.73],[7.82,6.72,1.32]),("T1","r1w1"):([1.63,1.72,1.73],[6.48,6.65,1.12]),
 ("T2","r0w0"):([1.68,1.70,1.71],[8.24,6.89,1.40]),("T2","r0w1"):([1.66,1.70,1.69],[8.02,6.94,1.30]),
 ("T2","r1w0"):([1.67,1.71,1.72],[8.15,6.90,1.42]),("T2","r1w1"):([1.66,1.72,1.69],[7.96,6.82,1.25])})
bk(4,"p15 Table 4","DR",{("T3","r0w0"):([1.79,1.78,1.62],[10.35,6.72,2.85]),("T3","r0w1"):([1.75,1.72,1.63],[9.64,6.72,2.26]),
 ("T3","r1w0"):([1.79,1.78,1.62],[9.85,6.85,2.30]),("T3","r1w1"):([1.75,1.72,1.63],[8.92,6.71,2.36]),
 ("T4","r0w0"):([1.79,1.78,1.62],[13.44,7.95,3.42]),("T4","r0w1"):([1.75,1.72,1.63],[12.89,8.24,3.55]),
 ("T4","r1w0"):([1.79,1.78,1.62],[12.76,8.36,3.21]),("T4","r1w1"):([1.75,1.72,1.63],[10.68,6.62,1.57])})
# Table 5 (wheat harvest 2002-03): BD_T, BD_D, K_T, K_D
t5 = {("t0","r0w0"):([1.68,1.69,1.61],[1.66,1.69,1.60],[12.82,7.52,2.85],[13.52,7.64,2.98]),
 ("t0","r0w1"):([1.66,1.70,1.59],[1.64,1.69,1.61],[12.90,7.57,3.20],[13.82,7.84,3.27]),
 ("t0","r1w0"):([1.66,1.70,1.60],[1.63,1.69,1.59],[12.95,7.96,3.20],[13.89,8.12,3.18]),
 ("t0","r1w1"):([1.65,1.69,1.59],[1.62,1.67,1.60],[13.18,6.44,1.85],[14.10,6.32,1.24]),
 ("t1","r0w0"):([1.67,1.69,1.60],[1.65,1.61,1.59],[12.51,7.44,1.26],[12.40,7.31,1.26]),
 ("t1","r0w1"):([1.66,1.69,1.60],[1.64,1.68,1.60],[12.70,6.62,2.15],[12.50,6.85,1.95]),
 ("t1","r1w0"):([1.65,1.70,1.61],[1.64,1.69,1.59],[12.82,6.65,2.60],[12.62,6.92,2.58]),
 ("t1","r1w1"):([1.65,1.70,1.60],[1.63,1.68,1.61],[12.96,7.14,2.50],[12.80,7.24,2.54])}
for (t,r),(bT,bD,kT,kD) in t5.items():
    for sysn,bb,kk in [("TR",bT,kT),("DR",bD,kD)]:
        for d,b_,k_ in zip(depths,bb,kk):
            add(f"{t}_{r} (wheat after {sysn})",d,"bulk_density_end",b_,"Mg/m3","p16 Table 5","table",g,"wheat harvest 2002-03")
            add(f"{t}_{r} (wheat after {sysn})",d,"sat_hydraulic_conductivity_end",k_,"cm/day","p16 Table 5","table",g,"wheat harvest 2002-03")
# infiltration text values (p19-p21)
for t,var,val,u,src,n in [
 ("T1 (TR)","initial_infiltration_rate","10-16","mm/hr","p18-p19","range over residue trts"),
 ("T2 (TR)","initial_infiltration_rate","18-22","mm/hr","p18-p19","range over residue trts"),
 ("T1r0w0 (TR)","final_infiltration_rate_300min",2.0,"mm/hr","p19",""),
 ("T2r1w1 (TR)","final_infiltration_rate_300min",4.0,"mm/hr","p19",""),
 ("T3r0w0 (DR)","initial_infiltration_rate",42,"mm/hr","p19",""),
 ("T4r1w1 (DR)","initial_infiltration_rate",58,"mm/hr","p19",""),
 ("T3 (DR)","final_infiltration_rate_300min",5.0,"mm/hr","p20",""),
 ("T4 (DR)","final_infiltration_rate_300min",6.0,"mm/hr","p20",""),
 ("t1 (wheat)","final_infiltration_rate_300min",5.0,"mm/hr","p20","text mm/hr but Fig 10/11 axes cm/hr (~0.5 cm/hr) - unit inconsistency"),
 ("t0 (wheat)","final_infiltration_rate_300min",4.0,"mm/hr","p20","same unit inconsistency")]:
    add(t,"surface",var,val,u,src,"text",g,n)

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
with open(OUT,"w",newline="",encoding="utf-8-sig") as fh:
    w = csv.writer(fh)
    w.writerow(["paper_name","site","treatment","depth_cm","variable","value","unit","source","confidence","category","note"])
    w.writerows(rows)
print(f"wrote {len(rows)} rows -> {OUT}")
