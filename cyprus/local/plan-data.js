'use strict';
// Image-space coordinates, not metres or geographic coordinates.
// Observed source labels: A01/A02 and B01/B02. No north/scale/revision supplied.
// Each floor drawing shows the pair: the 01 house on the left, the 02 house mirrored on the right.
// `split` = the party wall's x as a fraction of the image width (read from the pixels, 3.10.2026, local Claude fork);
// room points are on the 01 half, the 02 house mirrors them around `split`.
// B upper bed4 moved from [.34,.73] (wardrobe line) to [.44,.68] (the bed of the fourth bedroom), checked on b-upper.png.
const DUNE_PLANS = Object.freeze({
 site:{src:'/media/site.png',width:980,height:804,units:{
  A01:{points:'132,329 274,329 274,615 162,615 162,534 132,534',label:[211,493]},
  A02:{points:'274,329 414,329 414,532 384,532 384,615 274,615',label:[337,493]},
  B01:{points:'514,199 686,199 686,427 599,427 599,389 514,389',label:[602,320]},
  B02:{points:'686,199 856,199 856,389 772,389 772,427 686,427',label:[777,320]}}},
 pairs:{
  A:{ground:{src:'/media/a-ground.png',width:467,height:559,split:.503,rooms:[
    {id:'kitchen',at:[.24,.34],kind:'kitchen'},{id:'living',at:[.31,.58],kind:'living'},
    {id:'terrace',at:[.32,.15],kind:'terrace'},{id:'stairs',at:[.445,.6],kind:'stairs'}]},
   upper:{src:'/media/a-upper.png',width:491,height:559,split:.515,rooms:[
    {id:'bed1',at:[.35,.19],kind:'bed',number:1},{id:'bed2',at:[.34,.34],kind:'bed',number:2},
    {id:'bed3',at:[.29,.65],kind:'bed',number:3},{id:'bed4',at:[.35,.82],kind:'bed',number:4}]}},
  B:{ground:{src:'/media/b-ground.png',width:929,height:695,split:.498,rooms:[
    {id:'kitchen',at:[.17,.76],kind:'kitchen'},{id:'dining',at:[.17,.64],kind:'dining'},
    {id:'living',at:[.34,.28],kind:'living'},{id:'terrace',at:[.34,.09],kind:'terrace'}]},
   upper:{src:'/media/b-upper.png',width:980,height:788,split:.503,rooms:[
    {id:'bed1',at:[.33,.28],kind:'bed',number:1},{id:'bed2',at:[.16,.39],kind:'bed',number:2},
    {id:'bed3',at:[.15,.78],kind:'bed',number:3},{id:'bed4',at:[.44,.68],kind:'bed',number:4}]}}
 }
});
