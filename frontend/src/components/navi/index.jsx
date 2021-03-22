import React from 'react';

import { Grommet, Header, Anchor, Box, ResponsiveContext, Menu } from 'grommet';
import { Menu as MenuIcon, Test, Group, MapLocation } from 'grommet-icons';
import { grommet } from 'grommet/themes';



export const Navi = () => (
  <Grommet theme={grommet}>
    <Header background="light-5" pad="medium" height="xsmall">
      <Anchor
        href="https://hacktheclimate.devpost.com/"
        label="Hack The Climate 2021"
      />
      <Box  width='xsmall' height='xsmall'>
      </Box>
      <ResponsiveContext.Consumer>
        {size =>
          size === 'small' ? (
            <Box justify="end">
              <Menu
                a11yTitle="Navigation Menu"
                dropProps={{ align: { top: 'bottom', right: 'right' } }}
                icon={<MenuIcon color="brand" />}
                items={[
                  {
                    label: <Box pad="small">Home</Box>,
                    href: '/',
                  },
                  {
                    label: <Box pad="small">Scientifical Background</Box>,
                    href: '/science',
                  },
                  {
                    label: <Box pad="small">About</Box>,
                    href: '/about',
                  },
                ]}
              />
            </Box>
          ) : (
            <>
            <Box justify="end" direction="row" gap="medium">
              <Anchor icon={<MapLocation />} href="/" label="Home" />
              <Anchor icon={<Test />} href="/science" label="Scientifical Background" />
              <Anchor icon={<Group />} href="/about" label="About" />
            </Box>
            </>
          )
        }
      </ResponsiveContext.Consumer>
    </Header>
  </Grommet>
);

export default Navi;