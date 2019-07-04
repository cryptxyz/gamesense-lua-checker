from os import name, listdir, getcwd
from os.path import isfile, join
from time import time
from math import ceil
import re

if name != "nt":
	print( "[!] Please run this script on a windows machine." )
	exit( )

class check( ):
	def __init__( self ):
		self.forbidden_cvars = [ "sv_cheats", "mat_wireframe", "r_drawothermodels", "enable_skeleton_draw", "r_drawbeams", "r_drawbrushmodels", "r_drawdetailprops", "r_drawstaticprops", "r_modelwireframedecal", "r_shadowwireframe", "r_slowpathwireframe", "r_visocclusion", "vcollide_wireframe", "mp_radar_showall", "radarvisdistance", "mat_proxy", "mat_drawflat", "mat_norendering", "mat_drawgray", "mat_showmiplevels", "mat_showlowresimage", "mat_measurefillrate", "mat_fillrate", "mat_reversedepth", "fog_override", "r_drawentities", "r_drawdisp", "r_drawfuncdetail", "r_drawworld", "r_drawmodelstatsoverlay", "r_drawopaqueworld", "r_drawtranslucentworld", "r_drawopaquerenderables", "r_drawtranslucentrenderables", "mat_normals", "sv_allow_thirdperson", "sv_pure" ]
		self.lua_scripts = [ ]
		self.files = [ ]
		self.trusted = [ ]
		self.untrusted = [ ]
		self.compiled = [ ]
		self.path = getcwd( )
		self.time_started = time( )

	def get_luas( self ):
		self.files = [ f for f in listdir( self.path ) if isfile( join( self.path, f ) ) ]

		for file in self.files:
			if file[ ( len( file ) - 4 ): ] == ".lua":
				self.lua_scripts.append( file )
			elif file[ ( len( file ) - 5 ): ] == ".ljbc":
				self.compiled.append( file )

	def check_luas( self ):
		for lua in self.lua_scripts:
			found = False
			file = open( lua, "r" )
			lines = [ l.rstrip( "\n" ) for l in file ]
			for cvar in self.forbidden_cvars:
				for line in lines:
					reg = re.compile( "(.*\"{}\".*)".format( cvar ), re.I )
					result = reg.match( line )
					if result != None:
						found = True				

			if found == True:
				self.untrusted.append( lua )
			else:
				self.trusted.append( lua )


	def summary( self ):
		print( "[!] {} compiled lua scripts could not be checked".format( len( self.compiled ) ) )
		print( "[+] {} out of {} lua scripts are trusted".format( len( self.trusted ), len( self.lua_scripts ) ) )
		print( "[-] {} out of {} lua scripts are untrusted".format( len( self.untrusted ), len( self.lua_scripts ) ) )
		for ut in self.untrusted:
			print( "[-] {} is an untrusted script".format( ut ) )
		print( "[!] Finished in {} seconds".format( ceil( ( time( ) - self.time_started ) * 100 ) / 100 ) )




def main( ):
	print( "[!] gamesense lua checker by jonny5" )
	print( "[!] I don't take any responsibility for any banned accounts." )
	print( "[!] This script will fail checking string obfuscated lua scripts" )
	c = check( )
	c.get_luas( )
	c.check_luas( )
	c.summary( )

if __name__ == "__main__":
	main( )