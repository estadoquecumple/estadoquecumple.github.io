import { aggregate, coverage } from '../data/territorial/metrics-v3';
self.onmessage=(event:MessageEvent<{values:Array<number|null>}>)=>{
  self.postMessage({aggregate:aggregate(event.data.values),coverage:coverage(event.data.values)});
};
