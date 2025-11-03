// Simple header stub (optional)
    import React from 'react'
    export default function App(){
  return (
    <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'12px 20px',borderRadius:12,boxShadow:'0 6px 18px rgba(0,0,0,0.08)',background:'#fff'}}>
      <div style={{display:'flex',alignItems:'center'}}>
        <img src="/logo.png" alt="logo" style={{width:56,height:56,marginRight:12}}/>
        <div>
          <h2 style={{margin:0}}>Autosys Job Monitoring</h2>
          <small style={{color:'#666'}}>Live simulated dashboard • SLA & Dependency analysis</small>
        </div>
      </div>
      <div>
        <button style={{padding:'8px 14px',borderRadius:8,border:'none',cursor:'pointer'}}>Refresh</button>
      </div>
    </div>
  )
}
