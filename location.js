fetch('https://matteanalytics.com/save_event', {
    method: "POST",
    body: JSON.stringify({
        'event': window.location.href
    })
})