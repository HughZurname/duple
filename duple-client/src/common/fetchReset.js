const fetchReset = baseUrl =>
    fetch(`${baseUrl || 'http://localhost:8080'}/reset`, {
        headers: {
            clientId: window.localStorage.getItem('clientId'),
        },
    })

export default fetchReset
