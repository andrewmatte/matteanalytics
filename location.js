matteAnalyticsPing = () => {
    fetch('https://matteanalytics.com/save_event', {
        method: 'POST',
        body: JSON.stringify({
            'event': window.location.href,
            'referrer': document.referrer
        })
    })
}; matteAnalyticsPing();

window.onpopstate = matteAnalyticsPing;
window.onpushstate = (a,b,c) => {output=window.onpushstate(a,b,c);matteAnalyticsPing();return output};