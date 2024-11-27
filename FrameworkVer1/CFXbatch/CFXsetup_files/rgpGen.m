
% Generate .rgp file from REFPROP fluid data for ANSYS CFX
% The script is an adaptation of the RGP generator in LAMD GITLAB (/thermodynamics/rgp-generator).

function rgpGen(address, fld, P_min, P_max, T_min, T_max, Tsat_min, Tsat_max, nP, nT, nPsat)

    desc = strcat(fld,' from NIST REFPROP database');
    
    % Universal gas constant [J/kmol.K]
    R = 8314.4621;
    m = refpropm('M','T',300,'P',100,fld);
    r = R/m;
    
    Ttr = refpropm('T','R',0,'',0,fld);
    Tcr = refpropm('T','C',0,'',0,fld);
    Tmax = refpropm('T','M',0,'',0,fld)*3/2;
    Ptr = refpropm('P','R',0,'',0,fld)*1e3;
    Pcr = refpropm('P','C',0,'',0,fld)*1e3;
    Pmax = refpropm('P','M',0,'',0,fld)*1e3;
    
    dP_eff = (P_max-P_min)/(nP-1);
    P = P_min:dP_eff:P_max; %P(1) = 100;
    dT_eff = (T_max-T_min)/(nT-1);
    T = T_min:dT_eff:T_max;
    
    Psat_min = refpropm('P','T',Tsat_min,'Q',1,fld)*1e3;
    Psat_max = refpropm('P','T',Tsat_max,'Q',1,fld)*1e3;
    dPsat_eff = (Psat_max-Psat_min)/(nPsat-1);
    Psat = Psat_min:dPsat_eff:Psat_max;
    
    %% Tables data evaluation
    
    % Superheat data vectors preallocation
    h = zeros(1,nP*nT);
    a = zeros(1,nP*nT);
    v = zeros(1,nP*nT);
    cv = zeros(1,nP*nT);
    cp = zeros(1,nP*nT);
    dPdv = zeros(1,nP*nT);
    s = zeros(1,nP*nT);
    mu = zeros(1,nP*nT);
    kp = zeros(1,nP*nT);
    Ts = zeros(1,nP);
    hs = zeros(1,nP);
    as = zeros(1,nP);
    vs = zeros(1,nP);
    cvs = zeros(1,nP);
    cps = zeros(1,nP);
    dPdvs = zeros(1,nP);
    ss = zeros(1,nP);
    mus = zeros(1,nP);
    kps = zeros(1,nP);
    
    % Superheat data vectors evaluation
    for i = 1:nP
        if P(i) >= Pcr
            Ts(i) = 0; hs(i) = 0; as(i) = 0; vs(i) = 0; cvs(i) = 0; cps(i) = 0; dPdvs(i) = 0; ss(i) = 0; mus(i) = 0; kps(i) = 0;
        else
            [Ts(i),hs(i),as(i),rhos,cvs(i),cps(i),drhodPs,ss(i),mus(i),kps(i)] = refpropm('THADOCRSVL','P',P(i)/1e3,'Q',1,fld);
            drhodPs = drhodPs/1e3;
            vs(i) = 1/rhos;
            dPdvs(i) = -rhos^2/drhodPs;
            clear rhos drhodPs
        end
        for j = 1:nT
            if T(j) <= Ts(i)
                h(nT*(i-1)+j) = hs(i); a(nT*(i-1)+j) = as(i); v(nT*(i-1)+j) = vs(i); cv(nT*(i-1)+j) = cvs(i); cp(nT*(i-1)+j) = cps(i); dPdv(nT*(i-1)+j) = dPdvs(i); s(nT*(i-1)+j) = ss(i); mu(nT*(i-1)+j) = mus(i); kp(nT*(i-1)+j) = kps(i);
            else
                [h(nT*(i-1)+j),a(nT*(i-1)+j),rho,cv(nT*(i-1)+j),cp(nT*(i-1)+j),drhodP,s(nT*(i-1)+j),mu(nT*(i-1)+j),kp(nT*(i-1)+j)] = refpropm('HADOCRSVL','T',T(j),'P',P(i)/1e3,fld);
                drhodP = drhodP/1e3;
                v(nT*(i-1)+j) = 1/rho;
                dPdv(nT*(i-1)+j) = -rho^2/drhodP;
                clear rho drhodP
            end
        end
    end
    clear i j
    
    % Saturation data vectors preallocation
    Tsat = zeros(1,nPsat);
    h0 = zeros(1,nPsat);
    cp0 = zeros(1,nPsat);
    rho0 = zeros(1,nPsat);
    drhodP0 = zeros(1,nPsat);
    s0 = zeros(1,nPsat);
    cv0 = zeros(1,nPsat);
    a0 = zeros(1,nPsat);
    mu0 = zeros(1,nPsat);
    kp0 = zeros(1,nPsat);
    h1 = zeros(1,nPsat);
    cp1 = zeros(1,nPsat);
    rho1 = zeros(1,nPsat);
    drhodP1 = zeros(1,nPsat);
    s1 = zeros(1,nPsat);
    cv1 = zeros(1,nPsat);
    a1 = zeros(1,nPsat);
    mu1 = zeros(1,nPsat);
    kp1 = zeros(1,nPsat);
    
    % Saturation data vectors evaluation
    for k = 1:nPsat
        [Tsat(k),h0(k),cp0(k),rho0(k),drhodP0(k),s0(k),cv0(k),a0(k),mu0(k),kp0(k)] = refpropm('THCDRSOAVL','P',Psat(k)/1e3,'Q',0,fld);
        [Tsat(k),h1(k),cp1(k),rho1(k),drhodP1(k),s1(k),cv1(k),a1(k),mu1(k),kp1(k)] = refpropm('THCDRSOAVL','P',Psat(k)/1e3,'Q',1,fld);
    end
    clear k
    drhodP0 = drhodP0/1e3;
    drhodP1 = drhodP1/1e3;
    
    %% Parameters
    
    % Parameters
    param = cell(1);
    param{1,1} = '$$PARAM';
    param{2,1} = 26;
    param{3,1} = 'DESCRIPTION';
    param{4,1} = desc;
    param{5,1} = 'NAME';
    param{6,1} = fld;
    param{7,1} = 'INDEX';
    param{8,1} = fld;
    param{9,1} = 'MODEL';
    param{10,1} = 3;
    param{11,1} = 'UNITS';
    param{12,1} = 1;
    param{13,1} = 'GAS_CONSTANT';
    param{14,1} = r;
    param{15,1} = 'P_TRIPLE ';
    param{16,1} = Ptr;
    param{17,1} = 'P_CRITICAL';
    param{18,1} = Pcr;
    param{19,1} = 'T_TRIPLE';
    param{20,1} = Ttr;
    param{21,1} = 'T_CRITICAL';
    param{22,1} = Tcr;
    param{23,1} = 'PMIN_SUPERHEAT';
    param{24,1} = P_min;
    param{25,1} = 'PMAX_SUPERHEAT';
    param{26,1} = P_max;
    param{27,1} = 'TMIN_SUPERHEAT';
    param{28,1} = T_min;
    param{29,1} = 'TMAX_SUPERHEAT';
    param{30,1} = T_max;
    param{31,1} = 'TMIN_SATURATION';
    param{32,1} = Tsat_min;
    param{33,1} = 'TMAX_SATURATION';
    param{34,1} = Tsat_max;
    param{35,1} = 'TABLE_1';
    param{36,1} = [nT,nP];
    param{37,1} = 'TABLE_2';
    param{38,1} = [nT,nP];
    param{39,1} = 'TABLE_3';
    param{40,1} = [nT,nP];
    param{41,1} = 'TABLE_4';
    param{42,1} = [nT,nP];
    param{43,1} = 'TABLE_5';
    param{44,1} = [nT,nP];
    param{45,1} = 'TABLE_6';
    param{46,1} = [nT,nP];
    param{47,1} = 'TABLE_7';
    param{48,1} = [nT,nP];
    param{49,1} = 'TABLE_8';
    param{50,1} = [nT,nP];
    param{51,1} = 'TABLE_9';
    param{52,1} = [nT,nP];
    param{53,1} = 'SAT_TABLE';
    param{54,1} = [nPsat,4,9];
    
    %% Tables
    
    % Table 1: h [J/kg]
    table1 = cell(1);
    table1{1,1} = '$TABLE_1';
    table1{2,1} = [nT,nP];
    table1{3,1} = T;
    table1{4,1} = P;
    table1{5,1} = h;
    table1{6,1} = Ts;
    table1{7,1} = hs;
    
    % Table 2: a [m/s]
    table2 = cell(1);
    table2{1,1} = '$TABLE_2';
    table2{2,1} = [nT,nP];
    table2{3,1} = T;
    table2{4,1} = P;
    table2{5,1} = a;
    table2{6,1} = Ts;
    table2{7,1} = as;
    
    % Table 3: v [m^3/kg]
    table3 = cell(1);
    table3{1,1} = '$TABLE_3';
    table3{2,1} = [nT,nP];
    table3{3,1} = T;
    table3{4,1} = P;
    table3{5,1} = v;
    table3{6,1} = Ts;
    table3{7,1} = vs;
    
    % Table 4: cv [J/kg.K]
    table4 = cell(1);
    table4{1,1} = '$TABLE_4';
    table4{2,1} = [nT,nP];
    table4{3,1} = T;
    table4{4,1} = P;
    table4{5,1} = cv;
    table4{6,1} = Ts;
    table4{7,1} = cvs;
    
    % Table 5: cp [J/kg.K]
    table5 = cell(1);
    table5{1,1} = '$TABLE_5';
    table5{2,1} = [nT,nP];
    table5{3,1} = T;
    table5{4,1} = P;
    table5{5,1} = cp;
    table5{6,1} = Ts;
    table5{7,1} = cps;
    
    % Table 6: (dP/dv)_T [Pa.kg/m^3]
    table6 = cell(1);
    table6{1,1} = '$TABLE_6';
    table6{2,1} = [nT,nP];
    table6{3,1} = T;
    table6{4,1} = P;
    table6{5,1} = dPdv;
    table6{6,1} = Ts;
    table6{7,1} = dPdvs;
    
    % Table 7: s [J/kg.K]
    table7 = cell(1);
    table7{1,1} = '$TABLE_7';
    table7{2,1} = [nT,nP];
    table7{3,1} = T;
    table7{4,1} = P;
    table7{5,1} = s;
    table7{6,1} = Ts;
    table7{7,1} = ss;
    
    % Table 8: mu [Pa.s]
    table8 = cell(1);
    table8{1,1} = '$TABLE_8';
    table8{2,1} = [nT,nP];
    table8{3,1} = T;
    table8{4,1} = P;
    table8{5,1} = mu;
    table8{6,1} = Ts;
    table8{7,1} = mus;
    
    % Table 9: kp [W/m.K]
    table9 = cell(1);
    table9{1,1} = '$TABLE_9';
    table9{2,1} = [nT,nP];
    table9{3,1} = T;
    table9{4,1} = P;
    table9{5,1} = kp;
    table9{6,1} = Ts;
    table9{7,1} = kps;
    
    % Saturation table
    tables = cell(1);
    tables{1,1} = Psat;
    tables{2,1} = Tsat;
    tables{3,1} = zeros(size(Psat));
    tables{4,1} = zeros(size(Psat));
    tables{5,1} = h0;
    tables{6,1} = cp0;
    tables{7,1} = rho0;
    tables{8,1} = drhodP0;
    tables{9,1} = s0;
    tables{10,1} = cv0;
    tables{11,1} = a0;
    tables{12,1} = mu0;
    tables{13,1} = kp0;
    tables{14,1} = h1;
    tables{15,1} = cp1;
    tables{16,1} = rho1;
    tables{17,1} = drhodP1;
    tables{18,1} = s1;
    tables{19,1} = cv1;
    tables{20,1} = a1;
    tables{21,1} = mu1;
    tables{22,1} = kp1;
    
    %% File contents
    
    % Header header
    headerheader = cell(1);
    headerheader{1,1} = '$$$$HEADER';
    headerheader{2,1} = ['$$$',fld];
    headerheader{3,1} = 1;
    
    % Data header
    dataheader = cell(1);
    dataheader{1,1} = '$$$$DATA';
    dataheader{2,1} = ['$$$',fld];
    dataheader{3,1} = 1;
    
    % Superheat header
    suptabheader = cell(1);
    suptabheader{1,1} = '$$SUPER_TABLE';
    suptabheader{2,1} = 9;
    
    % Saturation header
    sattabheader = cell(1);
    sattabheader{1,1} = '$$SAT_TABLE';
    sattabheader{2,1} = [nPsat,4,9];
    
    % Header
    header = [headerheader;param];
    
    % Data
    data = [dataheader;param;suptabheader;table1;table2;table3;table4;table5;table6;table7;table8;table9;sattabheader;tables];
    
    % File content
    content = [header;data];
    
    %% .xlsx file writing
    
    % File name
    filename = [address,'\',fld,'.rgp'];
    
    % Writing
    dlmwrite(filename,content{1},'delimiter','');
    for l = 2:length(content)
        if ischar(content{l})
            dlmwrite(filename,content{l},'-append','delimiter','');
        else
            dlmwrite(filename,content{l},'-append','delimiter','\t','precision',6);
        end
    end

end
