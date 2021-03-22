import React from 'react';

import { Box, Card, CardBody, CardHeader, Heading, Image, Stack, Text } from 'grommet';




const SampleCard = (props) => {

    return (
        <>
            <Card margin='small' width="medium">
                <Stack anchor="bottom-left">
                    <CardBody height="medium">
                        <Image
                        fit="cover"
                        src={props.stage.image}
                        />
                    </CardBody>
                    <CardHeader
                        pad={{ horizontal: 'small', vertical: 'small' }}
                        background="#000000A0"
                        width="medium"
                        justify="start"
                    >
                        <Box>
                            <Heading level="3" margin="xxsmall">
                                {props.stage.id}
                            </Heading>
                            <Text size="small">{props.stage.title}</Text>
                        </Box>
                    </CardHeader>
                </Stack>
            </Card>
        </>
    );
};

export default SampleCard;