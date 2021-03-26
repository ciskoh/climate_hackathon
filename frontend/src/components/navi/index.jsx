import React, { useState } from 'react';

import { Anchor, Box, Header, Image,  Menu, ResponsiveContext } from 'grommet';
import { Menu as MenuIcon, Group, MapLocation, FingerPrint, BarChart } from 'grommet-icons';
import ClimateHackathon from '../../assets/logos/ClimateHackathon.png';



export const Navi = () => {
  const [ isSmallScreen, setIsSmallScreen ] = useState(false);
   return (
    <Header background="light-5" pad="medium" height="xsmall" elevation='small'>
      <Anchor
        href="https://hacktheclimate.devpost.com/"
        label="Hack The Climate 2021"
        icon={<Image src={ClimateHackathon} />}
      />  
      <ResponsiveContext.Consumer>
        {size =>
          size === 'medium' ? (
            <Box justify="end">
              {
                setIsSmallScreen(true)
              }
              <Menu
                a11yTitle="Navigation Menu"
                dropProps={{ align: { top: 'bottom', right: 'right' } }}
                icon={<MenuIcon color="brand" />}
                items={[
                  {
                    label: <Box pad="small">Home</Box>,
                    href: '/climate',
                  },

                  {
                    label: <Box pad="small">Map</Box>,
                    href: '/map',
                  },
                  {
                    label: <Box pad="small">Data Table</Box>,
                    href: '/analysis/',
                  },
                  {
                    label: <Box pad="small">The Team</Box>,
                    href: '/about/',
                  },
                ]}
              />
            </Box>
          ) : (
            <>
            {
              setIsSmallScreen(false)
            }
            <Box justify="end" direction="row" gap="medium">
              <Anchor icon={<FingerPrint />} href="/climate" label="Home" />
              <Anchor icon={<MapLocation />} href="/map" label="Map" />
              <Anchor icon={<BarChart />} href="/analysis/" label="Data Table" />
              <Anchor icon={<Group />} href="/about/" label="The Team" />
            </Box>
            </>
          )
        }
      </ResponsiveContext.Consumer>
    </Header>
  );
}
export default Navi;