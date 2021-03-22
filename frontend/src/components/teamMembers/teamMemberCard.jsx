import React, { useState } from 'react';

import { Box, Button, Card, CardBody, CardFooter, 
    Collapsible, Heading, Paragraph, Image } from 'grommet';
import { FormDown, FormUp, Linkedin } from 'grommet-icons';


const tempPhoto = 'https://static.vecteezy.com/system/resources/previews/002/086/401/original/cute-scientist-character-experiment-chemical-cartoon-icon-illustration-free-vector.jpg';


const TeamMemberCard = (props) => {

    const member = props.member; 
    const [open, setOpen] = useState(false);
    
    const ExpandButton = ({ ...rest }) => {
        const Icon = open ? FormUp : FormDown;
        return (
            <Button  
            hoverIndicator="light-4"
                icon={<Icon color="brand" />}
                {...rest}  
            />
        );
    };
    

    return (
        <>

                <Box pad="small" align="start" width='large'>
                    <Card elevation="large" width="large">
                        <CardBody height="small">
                            <Image
                                fit="cover"
                                fill
                                src={ member.image ? member.image : tempPhoto }
                            />
                            <Heading textAlign='center' alignSelf='center' level="4" margin={{ vertical: 'medium' }}>
                            {member.name}
                            </Heading>
                        </CardBody>
                        <Box pad={{ horizontal: 'medium' }} responsive={false}>
                            <Paragraph textAlign='center' size='medium' margin={{ top: 'small' }}>
                                {member.title}
                            </Paragraph>
                        </Box>
                        <CardFooter>
                            <Box direction="row" align="center" gap="small">

                            <Button icon={<Linkedin color='#0E76A8' size="medium" />} hoverIndicator />
                            </Box>
                            <ExpandButton onClick={() => setOpen(!open)} />
                        </CardFooter>
                        <Collapsible open={open}>
                            <Paragraph margin="medium" color="dark-3">
                                {member.personalInfo ? member.personalInfo : 'some personal info should be added'}
                            </Paragraph>
                        </Collapsible>
                    </Card>
                </Box>
        </>
    )
};
export default TeamMemberCard;