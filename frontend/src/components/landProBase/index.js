import firstImage from '../../assets/Landpro1.png';
import secondImage from '../../assets/Landpro2.png';
import thirdImage from '../../assets/Landpro3.png';

export const landproParagraphs = [

'Where does my crop grow well?',
'Which part of my park should I restore?', 
'What are the damages of the last fire, drought or flood?',
'Which part of this forest should be protected ?',
'Every day, farmers, construction companies, forest and park managers, environmental operators, environmental conscious tourists ask these kinds of questions, but the answers require long-term knowledge of the area and deep understanding of the ecosystem.', 
'By examining the spatial and temporal variability of vegetation, we combine image segmentation methods, with near-real time satellite data to get a quick evaluation of vegetated areas. ',
'Doing so improves dramatically the effectiveness and efficiency of environmental interventions at smaller as well as biger scales.', 
'Especialy usefull to support adaptive and sustainable agriculture management, monitor the evolution of the ecosystem after an intervention or an extreme event.', 
'LandPro tools can be distinctly useful to farmers and land administrators in developing regions, where the need for accurate, up-to-date data can help families produce more with smaller enviromental impact.'

];

export const howItWorks = [
    {
        id: 1,
        title: 'The user selects the area of interest via phone or computer using satellite RGB images as reference or using spatial vector files',
        image: firstImage,
    },
    {
        id: 2,
        title: 'The algorithm discriminates between different land cover / vegetation types using semantic segmentation',
        image: secondImage,
    },
    {
        id: 3,
        title: 'Infrared & radar data are used to classify the land productivity over time and space',
        image: thirdImage,
    },
];

export const referencedArticles = {
        articleName: 'Assessment of land degradation in Mediterranean forests and grazing lands using a landscape unit approach and the normalized difference vegetation index',
        link:'https://www.sciencedirect.com/science/article/abs/pii/S014362281630649X?via%3Dihub',
};
