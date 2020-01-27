import React from 'react'

import { Grommet, DataTable, CheckBox } from 'grommet'
import { grommet } from 'grommet/themes'

import TrainingPair from './TrainingPair'

const columns = [
    {
        property: 'pair_id',
        header: 'ID',
    },
    {
        property: 'records',
        header: 'Records',
        render: datum => (
            <TrainingPair
                record={datum.records.record}
                match={datum.records.match}
            />
        ),
    },
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
        <Grommet theme={grommet}>
            <DataTable
                style={{ width: '100%' }}
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
                        sortable: false,
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
                        sortable: false,
                    },
                ].map(col => ({ ...col }))}
                data={props.data}
            />
        </Grommet>
    )
}

export default TrainingTable
