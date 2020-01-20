import React from 'react'
import { useFetch } from '@bjornagh/use-fetch'

import { Grommet, Box, Button, Layer, Text } from 'grommet'
import { grommet } from 'grommet/themes'

// import { ReactComponent as Logo } from './logo.svg'

import useLocalStorage from './useLocalStorage'
import RoutedButton from './RoutedButton'
import TrainingTable from './TrainingTable'
import TrainingStatus from './TrainingStatus'

const Training = props => {
    const [positiveIds, setPositiveIds] = useLocalStorage('positiveIds', [])
    const [negativeIds, setNegativeIds] = useLocalStorage('negativeIds', [])
    const [attempts, setAttempts] = props.state.attempts

    const processMatches = (data, negativeIds, positiveIds) => ({
        match: reduceData(data, positiveIds),
        distinct: reduceData(data, negativeIds),
    })

    const reduceData = (data, ids) =>
        data.reduce((accumulator, currentValue) => {
            if (ids.includes(currentValue.pair_id))
                accumulator.push([
                    currentValue.records.record,
                    currentValue.records.match,
                ])
            return accumulator
        }, [])

    const getTraining = useFetch({
        url: 'http://localhost:8080/training',
    })
    const postTraining = useFetch({
        url: 'http://localhost:8080/training',
        method: 'POST',
        init: {
            headers: {
                'Content-type': 'application/json',
            },
        },
    })

    return (
        <Grommet theme={grommet}>
            <TrainingStatus
                state={{ positiveIds, negativeIds, attempts }}
                handleClear={() => {
                    setPositiveIds([])
                    setNegativeIds([])
                }}
                handleSubmit={() => {
                    postTraining
                        .doFetch({
                            body: processMatches(
                                getTraining.data,
                                negativeIds,
                                positiveIds
                            ),
                        })
                        .then(response => {
                            if (response.ok && attempts < 3) {
                                setAttempts(attempts + 1)
                                setPositiveIds([])
                                setNegativeIds([])
                                getTraining.doFetch()
                            }
                        })
                }}
            />
            {attempts > 3 && (
                <Layer full>
                    <Box
                        fill
                        background='light-1'
                        align='center'
                        justify='center'>
                        <Text>
                            Training completed. You will be redirected to the
                            downloads page to await your results.
                        </Text>
                        <Box
                            direction='row'
                            gap='small'
                            pad={{
                                vertical: 'small',
                                horizontal: 'medium',
                            }}>
                            <Button
                                label='New Session'
                                onClick={() =>
                                    getTraining.doFetch().then(setAttempts(0))
                                }
                            />
                            <RoutedButton primary to='/download' label='Okay' />
                        </Box>
                    </Box>
                </Layer>
            )}
            {getTraining.fetching && <Text>Loading...</Text>}
            {!getTraining.fetching && getTraining.data && (
                <TrainingTable
                    data={getTraining.data}
                    state={{
                        positiveIds: [positiveIds, setPositiveIds],
                        negativeIds: [negativeIds, setNegativeIds],
                    }}
                />
            )}
        </Grommet>
    )
}

export default Training
