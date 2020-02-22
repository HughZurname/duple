import React from 'react'
import { Grommet } from 'grommet'
import { grommet } from 'grommet/themes'

const Wrapper = ({ children }) => (
    <Grommet theme={grommet} full>
        {children}
    </Grommet>
)

export default Wrapper
