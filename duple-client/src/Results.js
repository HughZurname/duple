import React from 'react'
import { useFetch } from '@bjornagh/use-fetch'

import { Grommet, Box, Meter, DataTable, Button, Text } from 'grommet'
import { grommet } from 'grommet/themes'
import Loader from 'react-loader-spinner'

const Results = props => {
    const results = useFetch({
        url: 'http://localhost:8080/results',
    })
    const stats = useFetch({
        url: 'http://localhost:8080/stats',
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
                    <Button
                        gap='medium'
                        primary
                        label='Download'
                        href='http://localhost:8080/results/file'
                    />
                </Box>
                {stats.fetching && <Text>Loading...</Text>}
                {!stats.fetching && stats.data && (
                    <Box direction='column' align='center' gap='small'>
                        <Text
                            style={{ width: '8em', textAlign: 'end' }}
                            size='medium'>
                            {stats.data.duplicates}
                        </Text>
                        <Text style={{ width: '8em', textAlign: 'end' }}>
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
                    columns={[
                        { property: 'index', header: 'Index' },
                        { property: 'given_name', header: 'Given Name' },
                        { property: 'surname', header: 'Surname' },
                        { property: 'date_of_birth', header: 'Date of Birth' },
                        { property: 'sex', header: 'Sex' },
                        { property: 'cluster_id', header: 'Cluster' },
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
