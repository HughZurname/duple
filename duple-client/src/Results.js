import React from 'react'

import { Grommet, Box, Text, DataTable, CheckBox } from 'grommet'
import { grommet } from 'grommet/themes'

const Results = props => {
    return (
        <Grommet theme={grommet} full>
            <Box></Box>
            <DataTable />
            <Box></Box>
        </Grommet>
    )
}

export default Results
