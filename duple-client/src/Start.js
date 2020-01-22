import React from 'react'

import { Grommet, Box, RadioButtonGroup, Button } from 'grommet'
import { grommet } from 'grommet/themes'

import useSessionStorage from './useSessionStorage'
import RoutedButton from './RoutedButton'

const Start = props => {
    const [, setPositiveIds] = useSessionStorage('positiveIds')
    const [, setNegativeIds] = useSessionStorage('negativeIds')
    const [, setAttempts] = useSessionStorage('attempts')
    const [, setTrainingComplete] = useSessionStorage('trainingComplete')
    const [modelType, setModelType] = useSessionStorage('modelType')
    return (
        <Grommet theme={grommet}>
            <Box direction='row' justify='between' pad='medium'>
                <RadioButtonGroup
                    name='radio'
                    options={[
                        { label: 'Use pre-trained model', value: 'trained' },
                        { label: 'Train new model', value: 'new' },
                    ]}
                    value={modelType}
                    onChange={event => setModelType(event.target.value)}
                    {...props}
                />
            </Box>
            <Box
                direction='row'
                justify='center'
                gap='medium'
                margin={{ top: 'medium' }}>
                <Button label='Clear' onClick={() => setModelType(null)} />
                <Button
                    label='Reset'
                    onClick={() =>
                        fetch('http://localhost:8080/reset').then(response => {
                            if (response.ok) setTrainingComplete(false)
                            setNegativeIds([])
                            setPositiveIds([])
                            setAttempts(1)
                            setModelType(null)
                        })
                    }
                />
                <RoutedButton
                    to='/upload'
                    label='Start'
                    disabled={modelType === null}
                    primary
                />
            </Box>
        </Grommet>
    )
}

export default Start
