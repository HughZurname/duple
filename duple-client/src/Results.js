import React from 'react'
import { useFetch } from '@bjornagh/use-fetch'

import { Grommet, Box, Meter, DataTable, Button, Text } from 'grommet'
import { grommet } from 'grommet/themes'
import Loader from 'react-loader-spinner'

const Results = props => {
    const { data, fetching } = useFetch({
        url: 'http://localhost:8080/results',
    })
    return (
        <Grommet theme={grommet}>
            <Box direction='row' justify='between' pad='medium'>
                <Text
                    style={{ width: '8em', textAlign: 'start' }}
                    size='medium'>{`11123 records processed`}</Text>
                <Box direction='column' align='center' gap='small'>
                    <Button
                        gap='medium'
                        primary
                        label='Download'
                        onClick={() => console.log('Download!')}
                    />
                </Box>
                <Text
                    style={{ width: '8em', textAlign: 'end' }}
                    size='medium'>{`1000 duplicates found`}</Text>
            </Box>
            {fetching && (
                <Box align='center' margin='xlarge'>
                    <Loader type='Triangle' color='#7D4CDB' height={60} />
                </Box>
            )}
            {!fetching && data && (
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
                                                value: (
                                                    datum.confidence * 100
                                                ).toFixed(2),
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
                    data={data.data}
                />
            )}
        </Grommet>
    )
}

export default Results
