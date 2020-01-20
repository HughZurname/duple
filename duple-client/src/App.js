import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'

import { Grommet, Main, Box, Drop, Heading, Header } from 'grommet'
import { grommet } from 'grommet/themes'
import {
    Home,
    Notification,
    CloudUpload,
    CloudDownload,
    Robot,
} from 'grommet-icons'
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css'

import useLocalStorage from './useLocalStorage'
import RoutedAnchor from './RoutedAnchor'
import Training from './Training'
import Upload from './Upload'

function App() {
    const [openNotification, setOpenNotification] = React.useState()
    const [attempts, setAttempts] = useLocalStorage('attempts', 0)
    const notificationRef = React.useRef(null)

    return (
        <Router>
            <Grommet theme={grommet} full>
                <Header
                    direction='row'
                    align='center'
                    pad={{ vertical: 'xsmall', horizontal: 'medium' }}
                    justify='between'
                    background='brand'
                    style={{ zIndex: '1000' }}>
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
                            to='/download'
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
                <Main pad='small'>
                    <Switch>
                        <Route path='/training'>
                            <Training
                                state={{ attempts: [attempts, setAttempts] }}
                            />
                        </Route>
                        <Route path='/upload'>
                            <Upload />
                        </Route>
                        <Route path='/download'>
                            <Heading>Download</Heading>
                        </Route>
                        <Route path='/'>
                            <Heading>Home</Heading>
                        </Route>
                    </Switch>
                </Main>
            </Grommet>
        </Router>
    )
}

export default App
