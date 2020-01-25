import { useFetch } from '@bjornagh/use-fetch'

const useDupleFetch = ({ url, init = {}, ...rest }) => {
    const clientId = window.localStorage.getItem('clientId')
    const apiRoot = 'http://localhost:8080'
    const finalUrl = `${apiRoot}${url}`
    const finalHeaders = { ...init.headers }
    finalHeaders['clientId'] = clientId
    init.headers = finalHeaders

    return useFetch({
        url: finalUrl,
        init,
        cachePolicy: 'cache-and-network',
        ...rest,
    })
}

export default useDupleFetch
