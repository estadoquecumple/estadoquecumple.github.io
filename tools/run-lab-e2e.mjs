import { spawn } from 'node:child_process';

const server=spawn(process.execPath,['node_modules/astro/astro.js','preview','--host','127.0.0.1','--port','4321'],{stdio:['ignore','pipe','pipe']});
let serverOutput='';
server.stdout.on('data',(chunk)=>serverOutput+=chunk);
server.stderr.on('data',(chunk)=>serverOutput+=chunk);
const deadline=Date.now()+120_000;
while(Date.now()<deadline){
  try{const response=await fetch('http://127.0.0.1:4321/observatorio/laboratorio-territorial/');if(response.ok)break;}catch{}
  await new Promise((resolve)=>setTimeout(resolve,250));
}
if(Date.now()>=deadline){server.kill();console.error(`E2E SERVER ERROR\n${serverOutput}`);process.exit(1);}
const runner=spawn(process.execPath,['node_modules/@playwright/test/cli.js','test'],{stdio:'inherit'});
const code=await new Promise((resolve)=>runner.on('exit',(value)=>resolve(value??1)));
server.kill('SIGTERM');
await new Promise((resolve)=>{const timeout=setTimeout(resolve,2000);server.once('exit',()=>{clearTimeout(timeout);resolve();});});
process.exit(code);
