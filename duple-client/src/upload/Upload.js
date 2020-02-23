// ----------------------------------------------
// TODO: This needs up be updated with the right
// component when the PR related to this isssue
// is resolved. Will probsably need to be a form
// ----------------------------------------------
// https://github.com/grommet/grommet/issues/2535
// ----------------------------------------------

import React, { useCallback, useState, useEffect } from 'react'
import { useDropzone } from 'react-dropzone'

import { Box, Heading, Text, Button, Layer } from 'grommet'
import styled from 'styled-components'

import {
    RoutedButton,
    useSessionStorage,
    Wrapper,
    useDupleFetch,
} from '../common'

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

const FileDropzone = ({ files, setFiles, text, setText }) => {
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
        noClick: files.length,
    })

    useEffect(() => {
        if (acceptedFiles.length > 0)
            setText(
                acceptedFiles.map(file => `${file.path} (${file.size} bytes)`)
            )
    }, [acceptedFiles, setText])

    return (
        <Container
            {...getRootProps({
                isDragAccept,
                isDragReject,
            })}>
            <input data-testid='file-upload' {...getInputProps()} />
            <Text>{text}</Text>
        </Container>
    )
}

const BaseForm = props => {
    const formData = new FormData()
    const postData = useDupleFetch(props.postSettings)
    const [files, setFiles] = useState([])
    const [text, setText] = useState(
        'Drop your data file here, or click to select...'
    )

    const [uploadSuccess, setUploadSuccess] = useSessionStorage(
        'uploadSuccess',
        false
    )
    const [, setTrainingComplete] = useSessionStorage('trainingComplete')

    const handleSubmit = event => {
        event.preventDefault()
        files.forEach(file => {
            formData.append('duple_data', file)
        })
        postData.doFetch({ body: formData }).then(response => {
            if (response.ok) setUploadSuccess(true)
            if (props.trained) setTrainingComplete(true)
        })
    }

    return (
        <Wrapper>
            {uploadSuccess && (
                <Layer full>
                    <Box
                        fill
                        background='light-1'
                        align='center'
                        justify='center'
                        pad='small'>
                        <Text>{props.progressText}</Text>
                        <Box
                            direction='row'
                            gap='small'
                            pad={{
                                vertical: 'small',
                                horizontal: 'medium',
                            }}>
                            <Button
                                label='New Upload'
                                onClick={() => setUploadSuccess(false)}
                            />
                            {props.progressButton}
                        </Box>
                    </Box>
                </Layer>
            )}
            <Box fill align='center' pad='small'>
                <Box width='full'>
                    <Heading size='small'>Upload</Heading>
                    <form onSubmit={handleSubmit}>
                        <FileDropzone
                            files={files}
                            setFiles={setFiles}
                            text={text}
                            setText={setText}
                        />
                        <Box
                            direction='row'
                            justify='center'
                            gap='small'
                            margin={{ top: 'medium' }}>
                            <Button
                                label='Clear'
                                disabled={files.length === 0}
                                onClick={() => {
                                    setFiles([])
                                    setText(
                                        'Drop your data file here, or click to select...'
                                    )
                                }}
                            />
                            <Button
                                type='submit'
                                label='Upload'
                                primary
                                disabled={files.length === 0}
                            />
                        </Box>
                    </form>
                </Box>
            </Box>
        </Wrapper>
    )
}

const Upload = props => {
    const [modelType] = useSessionStorage('modelType')
    if (modelType === 'trained')
        return (
            <BaseForm
                data-testid='trained-upload'
                trained={true}
                clientId={props.clientId}
                postSettings={{
                    url: '/existing',
                    method: 'POST',
                }}
                progressButton={
                    <RoutedButton primary to='/results' label='Okay' />
                }
                progressText='Deduplication data file successfully uploaded, please wait while your data
                            is being scanned for duplicates. You will be redirected to the results page.'
            />
        )
    else
        return (
            <BaseForm
                data-testid='training-upload'
                clientId={props.clientId}
                postSettings={{
                    url: '/upload',
                    method: 'POST',
                }}
                progressButton={
                    <RoutedButton primary to='/training' label='Okay' />
                }
                progressText='Classification data successfully uploaded. Your data
                            is being processed and will be redirected to the
                            training page to begin training.'
            />
        )
}

export default Upload
