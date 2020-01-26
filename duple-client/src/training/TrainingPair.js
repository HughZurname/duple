import React from 'react'

import { Grommet, Box, Text } from 'grommet'
import { grommet } from 'grommet/themes'
import { UserExpert, UserAdd } from 'grommet-icons'

const TrainingPair = props => {
    return (
        <Grommet theme={grommet}>
            <Box gap='xsmall'>
                <Box
                    round
                    direction='row'
                    justify='between'
                    align='center'
                    basis='xxsmall'
                    background='dark-3'>
                    <UserExpert
                        size='2em'
                        color='light-1'
                        style={{ paddingLeft: '1em', paddingRight: '1em' }}
                    />
                    <Text style={{ width: '5em' }}>
                        {props.record.given_name}
                    </Text>
                    <Text style={{ width: '5em' }}>{props.record.surname}</Text>
                    <Text style={{ width: '6em' }}>
                        {props.record.date_of_birth}
                    </Text>
                    <Text style={{ width: '1.5em' }}>{props.record.sex}</Text>
                </Box>
                <Box
                    round
                    direction='row'
                    justify='between'
                    align='center'
                    basis='xxsmall'
                    background='light-2'>
                    <UserAdd
                        size='2em'
                        style={{ paddingLeft: '1em', paddingRight: '1em' }}
                    />
                    <Text style={{ width: '5em' }}>
                        {props.match.given_name}
                    </Text>
                    <Text style={{ width: '5em' }}>{props.match.surname}</Text>
                    <Text style={{ width: '6em' }}>
                        {props.match.date_of_birth}
                    </Text>
                    <Text style={{ width: '1.5em' }}>{props.match.sex}</Text>
                </Box>
            </Box>
        </Grommet>
    )
}

export default TrainingPair
