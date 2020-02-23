import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'

import { Main, Box, Drop, Heading, Header } from 'grommet'
import {
    Home,
    Notification,
    CloudUpload,
    CloudDownload,
    Robot,
} from 'grommet-icons'
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css'

import { RoutedAnchor, Wrapper } from '../common'

import { Setup } from '../setup'
import { Upload } from '../upload'
import { Training } from '../training'
import { Results } from '../results'

const App = props => {
    const [openNotification, setOpenNotification] = React.useState()
    const notificationRef = React.useRef(null)

    return (
        <Router>
            <Wrapper>
                <Header
                    direction='row'
                    align='center'
                    pad={{ vertical: 'xsmall', horizontal: 'medium' }}
                    justify='between'
                    background='brand'
                    style={{ zIndex: '1000' }}
                    data-testid='header'>
                    <Heading level={3} margin='none' color='white'>
                        <RoutedAnchor
                            to='/'
                            icon={<Home />}
                            hoverIndicator></RoutedAnchor>
                        <RoutedAnchor
                            to='/upload'
                            icon={<CloudUpload />}
                            hoverIndicator></RoutedAnchor>
                        <RoutedAnchor
                            to='/training'
                            icon={<Robot />}
                            hoverIndicator></RoutedAnchor>
                        <RoutedAnchor
                            to='/results'
                            icon={<CloudDownload />}
                            hoverIndicator></RoutedAnchor>
                    </Heading>
                    <Box ref={notificationRef}>
                        <RoutedAnchor
                            onClick={() =>
                                setOpenNotification(!openNotification)
                            }
                            icon={<Notification />}
                        />
                    </Box>
                </Header>
                {openNotification && (
                    <Drop
                        style={{ borderRadius: 15 }}
                        align={{ top: 'bottom', right: 'left' }}
                        target={notificationRef.current}>
                        <Box round pad='small'>
                            No new notifications
                        </Box>
                    </Drop>
                )}
                <Main>
                    <Switch>
                        <Route path='/training'>
                            <Training totalAttempts={4} />
                        </Route>
                        <Route path='/upload'>
                            <Upload clientId={props.clientId} />
                        </Route>
                        <Route path='/results'>
                            <Results />
                        </Route>
                        <Route path='/'>
                            <Setup />
                        </Route>
                    </Switch>
                </Main>
            </Wrapper>
        </Router>
    )
}

export default App
