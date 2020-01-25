import React from 'react'

import { Grommet, Box, Meter, DataTable, Button, Text } from 'grommet'
import { grommet } from 'grommet/themes'
import Loader from 'react-loader-spinner'

import { useDupleFetch, RoutedButton } from '../common'

const Results = props => {
    const [downloaded, setDownloaded] = React.useState(false)
    const results = useDupleFetch({
        url: '/results',
    })
    const stats = useDupleFetch({
        url: '/stats',
    })
    return (
        <Grommet theme={grommet}>
            <Box direction='row' justify='between' pad='medium'>
                {stats.fetching && <Text>Loading...</Text>}
                {!stats.fetching && stats.data && (
                    <Box direction='column' align='center' gap='small'>
                        <Text
                            style={{ width: '8em', textAlign: 'start' }}
                            size='medium'>
                            {stats.data.records}
                        </Text>
                        <Text style={{ width: '8em', textAlign: 'start' }}>
                            records processed
                        </Text>
                    </Box>
                )}
                <Box direction='column' align='center' gap='small'>
                    <Text
                        style={{ width: '8em', textAlign: 'center' }}
                        size='large'>
                        Results
                    </Text>
                    <Box direction='row' gap='medium'>
                        <Button
                            primary
                            disabled={results.fetching}
                            gap='medium'
                            label='Download'
                            href={`http://localhost:8080/results/file?clientId=${window.localStorage.getItem(
                                'clientId'
                            )}`}
                            onClick={() => setDownloaded(true)}
                        />
                        <RoutedButton
                            to='/'
                            disabled={!downloaded}
                            color='accent-1'
                            label='Done'
                        />
                    </Box>
                </Box>
                {stats.fetching && <Text>Loading...</Text>}
                {!stats.fetching && stats.data && (
                    <Box direction='column' align='center' gap='small'>
                        <Text
                            weight='bold'
                            style={{ width: '8em', textAlign: 'end' }}
                            size='medium'>
                            {stats.data.duplicates}
                        </Text>
                        <Text
                            weight='bold'
                            style={{ width: '8em', textAlign: 'end' }}>
                            duplicates found
                        </Text>
                    </Box>
                )}
            </Box>
            {results.fetching && (
                <Box align='center' margin='xlarge' gap='large'>
                    <Loader type='Triangle' color='#7D4CDB' height={60} />
                    <Text>
                        Please wait while your data is scanned for duplicates...
                    </Text>
                </Box>
            )}
            {!results.fetching && results.data && (
                <DataTable
                    size='full'
                    style={{ width: '100%' }}
                    sortable={true}
                    primaryKey={`${results.data.data.index}`}
                    columns={[
                        { property: 'cluster_id', header: 'Cluster' },
                        { property: 'given_name', header: 'Given Name' },
                        { property: 'surname', header: 'Surname' },
                        { property: 'date_of_birth', header: 'Date of Birth' },
                        { property: 'sex', header: 'Sex' },
                        {
                            property: 'confidence',
                            header: 'Confidence',
                            render: datum => (
                                <Box pad={{ vertical: 'xsmall' }}>
                                    <Meter
                                        values={[
                                            {
                                                value: datum.confidence * 100,
                                            },
                                        ]}
                                        thickness='medium'
                                        size='small'
                                        background='dark-3'
                                        round
                                    />
                                </Box>
                            ),
                        },
                    ]}
                    data={results.data.data}
                    step={50}
                />
            )}
        </Grommet>
    )
}

export default Results
