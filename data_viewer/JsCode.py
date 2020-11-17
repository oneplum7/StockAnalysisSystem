# -*- coding: utf-8 -*-
'''
JS 代码
'''

with open("res/Kline.json","r",encoding="utf8") as target:
    Kline_js =  target.read()


html = '''
<!DOCTYPE html>
<html style="height: 100%">
<head>
    <meta charset="UTF-8">
    <title>DaoYuan</title>
    <script type="text/javascript" src="qrc:///img/res/jquery.js"></script>
    <script type="text/javascript" src="qrc:///img/res/echarts4x.js"></script>
    <style>
        .k-box{
            top: 25px;
        }
        .ma-box{
            top: 55px;
        }
        .vol-box{
            top: 68%;
        }
        .macd-box{
            top: 82%;
        }
        .pos-box{
            position: absolute;
            font-size: 13px;
            left: 0px;
            z-index: 1;
            padding: 5px;
            color: #5a6881;
        }
        .p{
            padding: 0;
            margin': 0;
        }
    </style>
</head>
<body style="height: 100%; margin: 0">
    <div id="container" style="height: 100%"></div>
    <div class="k-box pos-box" id='Poskdata'></div>
    <div class="ma-box pos-box" id='Posmadata'></div>
    <div class="vol-box pos-box" id='Posvoldata'></div>
    <div class="macd-box pos-box" id='Posmacddata'></div>
    
    <script type="text/javascript">
        var PosKSelect = document.getElementById('Poskdata');
        var PosMaSelect = document.getElementById('Posmadata');
        var PosMacdSelect = document.getElementById('Posmacddata');
        var PosVolSelect = document.getElementById('Posvoldata');
    </script>

</body>
</html>
'''

Pos_Js = '''
function PosSelect(params) {
    let _this = this;
    _this.ma = {};
    for(i=0;i<params.length;i++){
        var el = params[i]
        switch (el.seriesIndex) {
            case 0:
                _this.datas = {
                    color: el.color,
                    date:{
                        name:"时间",
                        value: el.name
                    },
                    open: {
                        name: "开",
                        value: el.value[1]
                    },
                    close: {
                        name: "收",
                        value: el.value[2]
                    },
                    low: {
                        name: "低",
                        value: el.value[3]
                    },
                    heigh: {
                        name: "高",
                        value: el.value[4]
                    },
                    zhangd:{
                        name:"涨幅",
                        value:((el.value[2] - el.value[1]) / el.value[1] * 100).toFixed(2),
                        color: el.color,
                    },
                    zhenf:{
                        name:"振幅",
                        value:(Math.abs(el.value[4] - el.value[3]) / el.value[3] * 100).toFixed(2)
                    }
                };
                
                break;
                
            case 1:
                _this.ma.ma20 = {
                    name: "MA20",
                    value: el.value.toFixed(4),
                    color: el.color
                };
                break;
            case 2:
                _this.ma.ma60 = {
                    name: "MA60",
                    value: el.value.toFixed(4),
                    color: el.color
                };
                break;
            case 3:
                _this.ma.ma120 = {
                    name: "MA120",
                    value: el.value.toFixed(4),
                    color: el.color
                };
                break;
            case 4:
                break;
            case 5:
                break;
            case 6:
                break;
            case 7:
                _this.vol = {
                    name: el.seriesName,
                    value: el.value,
                    color: el.color
                }
                break;
            case 8:
                _this.macd.macd = {
                    name: el.seriesName,
                    value: el.value,
                    color: el.color
                }
                break;
            case 9:
                _this.macd.dif = {
                    name: el.seriesName,
                    value: el.value,
                    color: el.color
                }
                break;
            case 10:
                _this.macd.dea = {
                    name: el.seriesName,
                    value: el.value,
                    color: el.color
                }
                break;
            default:
                break;
        }
    }
    
    var objk = Object.keys(_this.datas);
    var ak = [];
    for(j=1;j<objk.length;j++){
        ak.push(`${_this.datas[objk[j]].name}:<span style="color:${_this.datas[objk[j]].color}">${_this.datas[objk[j]].value}</span>&nbsp;`)
    }
    PosKSelect.innerHTML = "<p>"+ak.join('')+"</p>";
        
    var objma = Object.keys(_this.ma);
    var ama=[];
    for(j=0;j<objma.length;j++){
        ama.push(`<span style="color:${_this.ma[objma[j]].color}">${_this.ma[objma[j]].name}:${_this.ma[objma[j]].value}</span>&nbsp;`);
    }
    PosMaSelect.innerHTML = ama.join('');
    PosVolSelect.innerHTML = `${_this.vol.name}:<span style="color:${_this.vol.color}">${_this.vol.value}</span>&nbsp;`;
    var objmacd = Object.keys(_this.macd);
    var acd = [];
    for(j=0;j<objmacd.length;j++){
        acd.push(`${_this.macd[objmacd[j]].name}:<span style="color:${_this.macd[objmacd[j]].color}">${_this.macd[objmacd[j]].value}</span>&nbsp;`)
    }
    PosMacdSelect.innerHTML = acd.join('');

}
'''

splitData = '''
    function splitData(rawData) {
        var datas = [];
        print("t1")
        var times = [];
        var vols = [];
        for (var i = 0; i < rawData.length; i++) {
            datas.push(rawData[i]);
            times.push(rawData[i][0]);
            print(rawData[i][0]);
            vols.push(rawData[i][4]);
        }
        return {
            datas: datas,
            times: times,
            vols: vols,
        };
        print("t2")
    }
'''


echart_init = '''
    var myChart = echarts.init(document.getElementById('container'), 'chalk', {renderer: 'canvas'});
'''

websize = '''
window.onresize = function () {
    myChart.resize();
}  
'''

Formula_js = '''
function ifma(){
    var mapush = [];
    if (MA1 != 0){
        mapush.push('MA'+MA1[1]);
    }
    if (MA2 != 0){
        mapush.push('MA'+MA2[1]);
    }
    if (MA3 != 0){
        mapush.push('MA'+MA3[1]);
    }
    if (MA4 != 0){
        mapush.push('MA'+MA4[1]);
    }
    if (MA5 != 0){
        mapush.push('MA'+MA5[1]);
    }
    if (MA6 != 0){
        mapush.push('MA'+MA6[1]);
    }
    //console.log(MA2[1]) 
    return mapush
}
/*
* 计算MA均线
* @param {number} dayCount MA时间窗口
* @param {array} data 输入数据
* @param {string} field [可选]计算字段配置
*/
function MA(dayCount,datas,field) {
    var ma,i,l,j,sum;
    ma=[];
    //判断不放在循环内，提升性能
    if(field){
        //有字段配置
        for(i = 0, l = datas.length; i < l; i++){
            if(i < dayCount - 1){
                ma.push(NaN);
                continue;
            }
            sum = 0;
            for(j = 0; j < dayCount; j++){
                sum += datas[i - j][field];
            }
            ma.push(sum/dayCount);
        }
    }else{
        //无字段配置
        for(i=0,l=datas.length;i<l;i++){
            if(i<dayCount-1){
                ma.push(NaN);
                continue;
            }
            sum=0;
            for(j=0;j<dayCount;j++){
                sum+=datas[i-j];
            }
            ma.push(sum/dayCount);
        }
    }
    return [ma,dayCount];
}

/*
* 计算EMA指数平滑移动平均线
* @param {number} n 时间窗口
* @param {array} data 输入数据
* @param {string} field 计算字段配置
*/
function EMA(n, datas, field) {
    var i, l, ema, a;
    a = 2 / (n + 1);
    if (field) {
        //二维数组
        ema = [datas[0][field]];
        for (i = 1, l = datas.length; i < l; i++) {
            ema.push((a * datas[i][field] + (1 - a) * ema[i - 1]).toFixed(4));
        }
    } else {
        //普通一维数组
        ema = [datas[0]];
        for (i = 1, l = datas.length; i < l; i++) {
            ema.push((a * datas[i] + (1 - a) * ema[i - 1]).toFixed(4));
        }
    }
    return ema;
}

/*
	* 计算MACD
	* @param {number} short 快速EMA时间窗口
	* @param {number} long 慢速EMA时间窗口
	* @param {number} mid dea时间窗口
	* @param {array} data 输入数据
	* @param {string} field 计算字段配置
	*/
function MACD(short, long, mid, datas, field) {
    var i, l, dif, dea, macd, result;
    result = {};
    dif = [];
    macd = [];
    var emaShort = EMA(short,datas,field);
    var emaLong = EMA(long,datas,field);
    for (i = 0, l = datas.length; i < l; i++) {
        dif.push((emaShort[i] - emaLong[i]).toFixed(4));
    }
    dea = EMA(mid, dif);
    for (i = 0, l = datas.length; i < l; i++) {
        macd.push(((dif[i] - dea[i]) * 2).toFixed(4));
    }
    result.dif = dif;
    result.dea = dea;
    result.macd = macd;
    return result;
}
'''