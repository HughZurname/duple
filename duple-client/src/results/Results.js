import React from 'react'
import { useMachine } from '@xstate/react'

import { Box, Meter, DataTable, Text } from 'grommet'
import Loader from 'react-loader-spinner'

import { Wrapper } from '../common'
import { Stats } from '../stats'

import resultsMachine from './resultsMachine'

const Results = ({ onResolve }) => {
    const [state, send, service] = useMachine(resultsMachine)

    switch (state.value) {
        case 'loading':
            return (
                <Wrapper>
                    <Stats />
                    <Box align='center' margin='xlarge' gap='large'>
                        <Loader type='Triangle' color='#7D4CDB' height={60} />
                        <Text>
                            Please wait while your data is scanned for
                            duplicates...
                        </Text>
                    </Box>
                </Wrapper>
            )
        case 'success':
            return (
                <Wrapper>
                    <Stats />
                    <DataTable
                        sortable={true}
                        primaryKey={`${state.context.data.index}`}
                        columns={[
                            { property: 'cluster_id', header: 'Cluster' },
                            { property: 'given_name', header: 'Given Name' },
                            { property: 'surname', header: 'Surname' },
                            {
                                property: 'date_of_birth',
                                header: 'Date of Birth',
                            },
                            { property: 'sex', header: 'Sex' },
                            {
                                property: 'confidence',
                                header: 'Confidence',
                                render: datum => (
                                    <Box pad={{ vertical: 'xsmall' }}>
                                        <Meter
                                            values={[
                                                {
                                                    value:
                                                        datum.confidence * 100,
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
                        data={state.context.data.data}
                        step={50}
                    />
                </Wrapper>
            )
        case 'failure':
            return (
                <Box align='center' margin='xlarge' gap='large'>
                    <Text>Request failed! Please retry.</Text>
                </Box>
            )
        default:
            return (
                <Box align='center' margin='xlarge' gap='large'>
                    <Text>
                        No duplicates found. Please try with another dataset
                    </Text>
                </Box>
            )
    }
}

export default Results
