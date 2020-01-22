import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

import { Grommet, Box, Heading, Text, Button, Layer } from 'grommet'
import { grommet } from 'grommet/themes'
import styled from 'styled-components'

import RoutedButton from './RoutedButton'
import useSessionStorage from './useSessionStorage'
import useDupleFetch from './useDupleFetch'

const getColor = props => {
    if (props.isDragAccept) return '#00e676'
    if (props.isDragReject) return '#ff1744'
    return '#eeeeee'
}

const Container = styled.div`
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    border-width: 2px;
    border-radius: 2px;
    border-color: ${props => getColor(props)};
    border-style: dashed;
    background-color: #fafafa;
    color: #bdbdbd;
    outline: none;
    transition: border 0.24s ease-in-out;
`

const FileDropzone = props => {
    const setFiles = props.setFiles

    const onDropAccepted = useCallback(
        acceptedFiles => {
            setFiles(acceptedFiles)
        },
        [setFiles]
    )

    const {
        getRootProps,
        getInputProps,
        isDragAccept,
        isDragReject,
        acceptedFiles,
    } = useDropzone({
        accept: 'text/csv, application/vnd.ms-excel',
        multiple: false,
        onDropAccepted,
    })

    const uploadText = files => {
        if (files.length > 0)
            return (
                <Text>
                    {files[0].path} ({files[0].size} bytes)
                </Text>
            )
        else return <Text>Drop your data file here, or click to select...</Text>
    }

    return (
        <Container
            {...getRootProps({
                isDragAccept,
                isDragReject,
            })}>
            <input {...getInputProps()} />
            {uploadText(acceptedFiles)}
        </Container>
    )
}

const UploadForm = props => {
    const formData = new FormData()
    const postData = useDupleFetch({
        url: '/upload',
        method: 'POST',
    })
    const [files, setFiles] = React.useState([])
    const [uploadSuccess, setUploadSuccess] = useSessionStorage(
        'uploadSuccess',
        false
    )

    const handleSubmit = event => {
        event.preventDefault()
        files.forEach(file => {
            formData.append('duple_data', file)
        })
        postData.doFetch({ body: formData }).then(response => {
            if (response.ok) setUploadSuccess(true)
        })
    }

    return (
        <Grommet theme={grommet}>
            {uploadSuccess && (
                <Layer full>
                    <Box
                        fill
                        background='light-1'
                        align='center'
                        justify='center'>
                        <Text>
                            Classification data successfully uploaded. Your data
                            is being processed and will be redirected to the
                            training page to begin training.
                        </Text>
                        <Box
                            direction='row'
                            gap='small'
                            pad={{
                                vertical: 'small',
                                horizontal: 'medium',
                            }}>
                            <Button
                                label='New Upload'
                                onClick={() => {
                                    fetch('http://localhost:8080/reset').then(
                                        response => {
                                            if (response.ok)
                                                setUploadSuccess(false)
                                        }
                                    )
                                }}
                            />
                            <RoutedButton primary to='/training' label='Okay' />
                        </Box>
                    </Box>
                </Layer>
            )}
            <Box fill align='center' justify='center'>
                <Box width='full'>
                    <Heading size='small'>Upload</Heading>
                    <form onSubmit={handleSubmit}>
                        <FileDropzone setFiles={setFiles} />
                        <Box
                            direction='row'
                            justify='center'
                            gap='small'
                            margin={{ top: 'medium' }}>
                            <Button type='submit' label='Upload' primary />
                        </Box>
                    </form>
                </Box>
            </Box>
        </Grommet>
    )
}

export default UploadForm
