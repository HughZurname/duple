import React from 'react'

import { Grommet, Box, Layer, Text } from 'grommet'
import { grommet } from 'grommet/themes'
import Loader from 'react-loader-spinner'

import useSessionStorage from './useSessionStorage'
import useDupleFetch from './useDupleFetch'
import RoutedButton from './RoutedButton'
import TrainingTable from './TrainingTable'
import TrainingStatus from './TrainingStatus'

const Training = props => {
    const [positiveIds, setPositiveIds] = useSessionStorage('positiveIds', [])
    const [negativeIds, setNegativeIds] = useSessionStorage('negativeIds', [])
    const [attempts, setAttempts] = useSessionStorage('attempts', 0)
    const [trainingComplete, setTrainingComplete] = useSessionStorage(
        'trainingComplete',
        false
    )

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

    const getTraining = useDupleFetch({
        url: '/training',
    })
    const postTraining = useDupleFetch({
        url: '/training',
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
                positiveIds={positiveIds}
                negativeIds={negativeIds}
                attempts={attempts}
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
                            if (response.ok) {
                                if (attempts < 3) {
                                    setAttempts(attempts + 1)
                                    setPositiveIds([])
                                    setNegativeIds([])
                                    getTraining.doFetch()
                                } else setTrainingComplete(true)
                            }
                        })
                }}
            />
            {trainingComplete && (
                <Layer full>
                    <Box
                        fill
                        background='light-1'
                        align='center'
                        justify='center'>
                        <Text>
                            Training completed. You will be redirected to the
                            results page to await your results.
                        </Text>
                        <Box
                            direction='row'
                            gap='small'
                            pad={{
                                vertical: 'small',
                                horizontal: 'medium',
                            }}>
                            <RoutedButton
                                label='New Session'
                                to='/upload'
                                onClick={() => {
                                    if (trainingComplete)
                                        fetch(
                                            'http://localhost:8080/reset'
                                        ).then(response => {
                                            if (response.ok) setAttempts(0)
                                            setTrainingComplete(false)
                                        })
                                }}
                            />
                            <RoutedButton primary to='/results' label='Okay' />
                        </Box>
                    </Box>
                </Layer>
            )}
            {getTraining.fetching && (
                <Box align='center' margin='xlarge' gap='large'>
                    <Loader type='Triangle' color='#7D4CDB' height={60} />
                    <Text>
                        Please wait while the training model is updated and
                        unlabeled examples are retrieved...
                    </Text>
                </Box>
            )}
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
