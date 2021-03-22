import React from 'react';
import Navi from "../components/navi";
import { Anchor, Box, Heading, Paragraph } from 'grommet';


import { howItWorks, landproParagraphs, referencedArticles } from '../components/landProBase';
import SampleCard from '../components/landProBase/sampleCard';

const SciencePage = () => {
    return (
        <>
            <Navi />
            <Box  margin='medium' flex direction='column' >
                <Box width='85%' alignSelf='center'>
                    {landproParagraphs.map((paragraph, index) => (
                    <Paragraph fill key={index} size='medium' textAlign='center'>
                        {paragraph}
                    </Paragraph>
                    ))}
                </Box>

            <Heading level='2' margin="medium">How does it work?</Heading>

                <Box flex direction='row' width='85%' justify='center' alignSelf='center' >
                    {howItWorks.map((stage, index) => (
                        <SampleCard stage={stage} key={index}/>
                    ))}
                </Box>
            <Paragraph>Based on <Anchor href={referencedArticles.link} title={referencedArticles.name} label='this' /> publication </Paragraph>
            
            </Box>
        </>
    );
};

export default SciencePage;