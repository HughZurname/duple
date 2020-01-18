import React from 'react'

import { Grommet, Box, Text, DataTable, CheckBox } from 'grommet'
import { grommet } from 'grommet/themes'
import { UserExpert, UserAdd } from 'grommet-icons'

const columns = [
    {
        property: 'pair_id',
        header: 'ID'
    },
    {
        property: 'records',
        header: 'Records',
        render: datum => (
            <Box gap='xsmall'>
                <Box round direction='row' justify='between' align='center' basis='xxsmall' background='dark-3'>
                    <UserExpert size='2em' color='light-1' style={{ paddingLeft: '1em', paddingRight: '1em' }}/>
                    <Text style={{ width: '5em' }}>
                        {datum.records.record.given_name}
                    </Text>
                    <Text style={{ width: '5em' }}>
                        {datum.records.record.surname}
                    </Text>
                    <Text style={{ width: '6em' }}>
                        {datum.records.record.date_of_birth}
                    </Text>
                    <Text style={{ width: '1.5em' }}>
                        {datum.records.record.sex}
                    </Text>
                </Box>
                <Box round direction='row' justify='between' align='center' basis='xxsmall' background='light-2'>
                    <UserAdd size='2em' style={{ paddingLeft: '1em', paddingRight: '1em' }}/>
                    <Text style={{ width: '5em' }}>
                        {datum.records.match.given_name}
                    </Text>
                    <Text style={{ width: '5em' }}>
                        {datum.records.match.surname}
                    </Text>
                    <Text style={{ width: '6em' }}>
                        {datum.records.match.date_of_birth}
                    </Text>
                    <Text style={{ width: '1.5em' }}>
                        {datum.records.match.sex}
                    </Text>
                </Box>
            </Box>
        )
    }
]

const TrainingTable = props => {
    const [positiveIds, setPositiveIds] = props.state.positiveIds
    const [negativeIds, setNegativeIds] = props.state.negativeIds

    const onPositive = (event, value) => {
        if (event.target.checked && negativeIds.indexOf(value) === -1) {
            setPositiveIds([...positiveIds, value])
        } else {
            setPositiveIds(positiveIds.filter(item => item !== value))
        }
    }

    const onNegative = (event, value) => {
        if (event.target.checked && positiveIds.indexOf(value) === -1) {
            setNegativeIds([...negativeIds, value])
        } else {
            setNegativeIds(negativeIds.filter(item => item !== value))
        }
    }

    return (
        <Grommet theme={grommet} full>
            <DataTable
                columns={[
                    ...columns,
                    {
                        property: 'positiveIds',
                        render: datum => (
                            <CheckBox
                                key={datum.pair_id}
                                checked={
                                    positiveIds.indexOf(datum.pair_id) !== -1
                                }
                                onChange={e => onPositive(e, datum.pair_id)}
                            />
                        ),
                        header: 'Correct',
                        sortable: false
                    },
                    {
                        property: 'negativeIds',
                        render: datum => (
                            <CheckBox
                                key={datum.pair_id}
                                checked={
                                    negativeIds.indexOf(datum.pair_id) !== -1
                                }
                                onChange={e => onNegative(e, datum.pair_id)}
                            />
                        ),
                        header: 'Incorrect',
                        sortable: false
                    }
                ].map(col => ({ ...col }))}
                data={props.data}
            />
        </Grommet>
    )
}

export default TrainingTable
