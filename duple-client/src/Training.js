import React from 'react'
import { Grommet, Box, Layer, Button, Text } from 'grommet'
import { grommet } from 'grommet/themes'

import RoutedButton from './RoutedButton'
import TrainingTable from './TrainingTable'
import TrainingStatus from './TrainingStatus'

const Training = props => {
    const [positiveIds, setPositiveIds] = React.useState([])
    const [negativeIds, setNegativeIds] = React.useState([])
    const [attempts, setAttempts] = React.useState(0)
    const [data, setData] = React.useState([])

    React.useEffect(() => {
        fetch('http://localhost:8080/training')
            .then(response => {
                return response.json()
            })
            .then(resultData => {
                setData(resultData)
            })
    }, [setData])

    const handleClear = () => {
        setPositiveIds([])
        setNegativeIds([])
    }

    const handleSubmit = () => {
        fetch('http://localhost:8080/matching', {
            method: 'post',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(processMatches(data, negativeIds, positiveIds))
        })
            .then(response => {
                setAttempts(attempts + 1)
                handleClear()
                return response.json()
            })
            .then(resultData => {
                setData(resultData)
            })
    }

    const processMatches = (data, negativeIds, positiveIds) => ({
        match: reduceData(data, positiveIds),
        distinct: reduceData(data, negativeIds)
    })

    const reduceData = (data, ids) =>
        data.reduce((accumulator, currentValue) => {
            if (ids.includes(currentValue.pair_id))
                accumulator.push([
                    currentValue.records.record,
                    currentValue.records.match
                ])
            return accumulator
        }, [])

    return (
        <Grommet theme={grommet}>
            <TrainingStatus
                state={{
                    positiveIds: [positiveIds, setPositiveIds],
                    negativeIds: [negativeIds, setNegativeIds],
                    attempts: [attempts, setAttempts]
                }}
                handleSubmit={handleSubmit}
                handleClear={handleClear}
            />

            <TrainingTable
                data={data}
                state={{
                    positiveIds: [positiveIds, setPositiveIds],
                    negativeIds: [negativeIds, setNegativeIds]
                }}
            />
            {attempts === 3 && (
                <Layer full animation='fadeIn'>
                    <Box
                        fill
                        background='light-1'
                        align='center'
                        justify='center'>
                        <Text>
                            Training completed. You will be redirected to the homepage to await your results.
                        </Text>
                        <Box
                            direction='row'
                            gap='small'
                            pad={{
                                vertical: 'small',
                                horizontal: 'medium'
                            }}>
                            <RoutedButton
                                primary
                                to='/'
                                label='Okay'
                                onClick={() => {
                                    setData([])
                                    handleClear()
                                }}
                            />
                        </Box>
                    </Box>
                </Layer>
            )}
        </Grommet>
    )
}

export default Training
